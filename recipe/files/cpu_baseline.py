"""Fail the vendor build when the Polars runtime this environment loads needs more than x86-64-v2.

polars 1.34+ is a pure-Python package over one of three runtime wheels, and loads the first one installed in the
order compat, 64, 32 (polars/_plr.py). polars itself requires polars-runtime-32, which is built for x86-64-v3
(BUILD_FEATURE_FLAGS: AVX, AVX2, FMA, BMI1, BMI2, LZCNT, MOVBE, PCLMULQDQ). Its bundled jemalloc runs BMI2 code
(shlx in je_sc_data_init) while the library loads, so `import polars` dies with SIGILL on a CPU without them, before
Polars' own CPU check can do more than warn. PostHog's URL conf imports clickhouse_connect, which imports polars when it is
installed, so `manage.py check` and the web app load it: chain 804's vendor build died with exit code 132 on <redacted: internal host>
(Xeon E5-4650, no AVX2) on 2026-10-31. polars-runtime-compat, the same release built for x86-64-v2 (SSE3,
SSSE3, SSE4.1, SSE4.2, POPCNT, CMPXCHG16B), is installed beside it, so every PostHog process loads that one.

Usage: python cpu_baseline.py   (exits 0 when polars is absent, or loads a runtime built for x86-64-v2 or lower)."""
import importlib.util
import sys

# The x86-64-v3 additions over v2 (the x86-64 psABI micro-architecture levels), in Polars' flag spelling.
X86_64_V3 = {"avx", "avx2", "bmi1", "bmi2", "f16c", "fma", "lzcnt", "movbe", "xsave"}


def needed_flags(feature_flags):
    """The CPU features a BUILD_FEATURE_FLAGS string ('+sse3,+avx2,...') says the binary was built with."""
    return {f.strip().lstrip("+") for f in (feature_flags or "").split(",") if f.strip() and not f.strip().startswith("-")}


def check(find_spec=importlib.util.find_spec, import_module=__import__):
    """Returns (ok, message). Reads the compat runtime's declared flags before anything loads native code, so on an
    old CPU it reports instead of dying of SIGILL itself."""
    if find_spec("polars") is None:
        return True, "cpu baseline: polars is not installed"
    if find_spec("_polars_runtime_compat") is None:
        return False, ("cpu baseline: polars-runtime-compat is not installed, so polars loads polars-runtime-32, built "
                       "for x86-64-v3 (it dies with SIGILL without AVX2): install polars-runtime-compat at polars' version")
    import_module("_polars_runtime_compat")  # its __init__ is pure Python: BUILD_FEATURE_FLAGS, no native code
    flags = needed_flags(getattr(sys.modules["_polars_runtime_compat"], "BUILD_FEATURE_FLAGS", ""))
    above = sorted(flags & X86_64_V3)
    if above:
        return False, f"cpu baseline: _polars_runtime_compat is built with {', '.join(above)} (above x86-64-v2)"
    import_module("polars._plr")
    runtime = getattr(sys.modules["polars._plr"], "RUNTIME_REPR", None)
    if runtime != "rtcompat":
        return False, (f"cpu baseline: polars loads runtime {runtime!r}, not polars-runtime-compat (POLARS_FORCE_PKG or "
                       "POLARS_PREFER_PKG set?)")
    return True, f"cpu baseline: polars runtime {runtime} (_polars_runtime_compat), built with {', '.join(sorted(flags)) or 'no extra flags'}"


if __name__ == "__main__":
    ok, msg = check()
    print(msg, file=sys.stdout if ok else sys.stderr)
    sys.exit(0 if ok else 1)
