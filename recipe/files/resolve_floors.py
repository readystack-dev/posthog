"""Find the smallest set of upstream pins to relax so the CVE floors resolve: start from upstream's exact pins
(uv export), drop the pin of every floored package, then, while uv reports a conflict 'X==a depends on Y==b', relax X
to '>=a' (never a downgrade). Prints the resolved upgrades (name old -> new) and writes the relaxed requirement set."""
import os, re, subprocess, sys
req, floors, out = sys.argv[1], sys.argv[2], sys.argv[3]
norm = lambda n: re.sub(r"[-_.]+", "-", n).lower()
pins = {}
lines = []
for ln in open(req):
    m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(\[[^\]]*\])?==([^\s;]+)(.*)$", ln.strip())
    lines.append((m and norm(m.group(1)), ln.rstrip("\n"), m))
    if m:
        pins[norm(m.group(1))] = m.group(3)
fl = [l.strip() for l in open(floors) if l.strip() and not l.startswith("#")]
relaxed = {norm(re.split(r"[<>=!~ ]", f, maxsplit=1)[0]) for f in fl}
for it in range(40):
    body = []
    for n, ln, m in lines:
        if n and n in relaxed:
            if n in pins and not any(norm(re.split(r"[<>=!~ ]", f, maxsplit=1)[0]) == n for f in fl):
                body.append(f"{m.group(1)}{m.group(2) or ''}>={m.group(3)}{m.group(4)}")
            continue
        body.append(ln)
    open(out, "w").write("\n".join(body + fl) + "\n")
    pkg_cutoffs = [x for p in os.environ.get("RF_EXCLUDE_NEWER_PACKAGES", "").split() for x in ("--exclude-newer-package", p)]
    r = subprocess.run(["uv", "pip", "install", "--exclude-newer", os.environ["RF_EXCLUDE_NEWER"], *pkg_cutoffs,
                        "--resolution", "lowest-direct", "--dry-run", "-r", out],
                       capture_output=True, text=True)
    err = r.stderr
    if r.returncode == 0:
        ups = re.findall(r"^ - (\S+)==(\S+)\n \+ (\S+)==(\S+)", err, re.M)
        chg = [l for l in err.splitlines() if l.startswith((" - ", " + "))]
        print("RESOLVED after relaxing:", sorted(relaxed - {norm(re.split(r"[<>=!~ ]", f, maxsplit=1)[0]) for f in fl}))
        print("\n".join(chg))
        sys.exit(0)
    m = re.findall(r"you require ([A-Za-z0-9][A-Za-z0-9._-]*)==", err) + \
        re.findall(r"([A-Za-z0-9][A-Za-z0-9._-]*)==[^\s]+ depends on", err)
    cand = [norm(x) for x in m if norm(x) not in relaxed and norm(x) in pins]
    if not cand:
        print("UNRESOLVED:", err[-1500:]); sys.exit(1)
    print(f"round {it}: relax {cand[0]} ({pins.get(cand[0])})", flush=True)
    relaxed.add(cand[0])
