"""Fail the vendor build when a copy of a package in the deployed Node tree is still below its npm-floors.json floor.

npm-floors.json's overrides are merged into upstream's pnpm-workspace.yaml (Dockerfile.vendor). An override that does
not take (a key that does not replace upstream's own entry for the package, a selector that misses the installed range)
leaves the old copy in node_modules, and only the verdict hours later would show it (L-A154: a floor channel comes with
a check that each floor took). Chain 804 (2026-11-01): node-forge 1.4.0 shipped under upstream's own override
node-forge >=1.4.0; the floor >=1.4.1 replaces that entry.

Every copy the key selects is at or above the lowest version of the value ('^1.14.5', '>=4.0.6 <5', '1.22.0'): a key
`name` selects every copy, `name@<range>` the copies inside that range ('>=6 <6.28.1', '<0.35.5', '^5'). A key with a
parent selector (`a>b`) is not checked (npm-floors.json has none).

Usage: python3 npm_floors_check.py npm-floors.json <node_modules/.pnpm>   (exit 0: every floor took; 1: a copy below)"""
import glob
import json
import os
import re
import sys

_VER = re.compile(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?(-[0-9A-Za-z.-]+)?")


def ver(s):
    """A comparable key for a version or a (partial) range bound: (major, minor, patch, 0 for a prerelease else 1)."""
    m = _VER.search(str(s))
    if not m:
        raise ValueError(f"no version in {s!r}")
    return (int(m.group(1)), int(m.group(2) or 0), int(m.group(3) or 0), 0 if m.group(4) else 1)


def split_key(key):
    """(package name, selector range or None) of an overrides key: 'undici@>=6 <6.28.1', '@grpc/grpc-js@>=1 <1.14.5'."""
    at = key.find("@", 1)
    return (key, None) if at < 0 else (key[:at], key[at + 1:])


def _caret_tilde(c):
    """'^5' / '^0.4.9' / '~1.2.3' as their two comparators (semver: ^ keeps the first non-zero part, ~ the minor)."""
    op, b = c[0], c[1:]
    parts = [int(x) for x in re.findall(r"\d+", b)[:3]]
    lo = (parts + [0, 0, 0])[:3]
    if op == "~":
        hi = (lo[0] + 1, 0, 0) if len(parts) == 1 else (lo[0], lo[1] + 1, 0)
    elif lo[0] or len(parts) == 1:
        hi = (lo[0] + 1, 0, 0)
    elif lo[1] or len(parts) == 2:
        hi = (0, lo[1] + 1, 0)
    else:
        hi = (0, 0, lo[2] + 1)
    return [">=" + ".".join(map(str, lo)), "<" + ".".join(map(str, hi))]


def in_range(v, rng):
    """Whether version key v satisfies every comparator of a space-separated range ('>=6 <6.28.1', '<0.35.5', '^5',
    '2.0.0')."""
    cs = []
    for c in rng.split():
        cs += _caret_tilde(c) if c[:1] in "^~" else [c]
    for c in cs:
        m = re.match(r"(>=|<=|>|<|=)?\s*(.+)", c)
        op, b = m.group(1) or "=", ver(m.group(2))
        if not {">=": v >= b, "<=": v <= b, ">": v > b, "<": v < b, "=": v[:3] == b[:3]}[op]:
            return False
    return True


def copies(store, name):
    """[(version, path)] of every installed copy of `name` in a pnpm virtual store: the package's own directory under
    each .pnpm/<entry>/node_modules/ (the other entries there are symlinks to their own store directories)."""
    out = []
    for d in sorted(glob.glob(os.path.join(store, "*", "node_modules", *name.split("/")))):
        pj = os.path.join(d, "package.json")
        if os.path.islink(d) or not os.path.isfile(pj):
            continue
        try:
            v = json.load(open(pj)).get("version")
        except (OSError, ValueError):
            v = None
        if v:
            out.append((v, d))
    return out


def check(floors, store):
    """[(key, version, path, why)] for every copy an override should have moved and did not."""
    bad = []
    for key, value in floors.items():
        name, sel = split_key(key)
        if ">" in name:
            continue
        floor = ver(value)
        for v, path in copies(store, name):
            k = ver(v)
            if (sel is None or in_range(k, sel)) and k < floor:
                bad.append((key, v, path, f"below the floor {value}"))
    return bad


if __name__ == "__main__":
    floors = json.load(open(sys.argv[1]))["overrides"]
    store = sys.argv[2]
    if not os.path.isdir(store):
        print(f"npm floors: {store} is not a pnpm virtual store", file=sys.stderr)
        sys.exit(1)
    bad = check(floors, store)
    for key, v, path, why in bad:
        print(f"npm floors: {key} did not take: {os.path.relpath(path, store)} is {v}, {why}", file=sys.stderr)
    if not bad:
        print(f"npm floors: all {len(floors)} took in {store}")
    sys.exit(1 if bad else 0)
