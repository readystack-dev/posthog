set -e
cd "${CE_ROOT:-/code}"
python3 - <<'PY'
# ReadyStack CE: register the "ee" app label from the CE compatibility package, and load its settings, when PostHog's
# Enterprise package is absent. Each edit asserts the upstream text it replaces, so a moved upstream block fails the build.
edits = {
    "posthog/settings/web.py": [(
        'except ImportError:\n    pass\nelse:\n    INSTALLED_APPS.append("ee.apps.EnterpriseConfig")',
        'except ImportError:\n    INSTALLED_APPS.append("ee.ce.ReadyStackCEConfig")  # ReadyStack CE: app label "ee", no Enterprise code\nelse:\n    INSTALLED_APPS.append("ee.apps.EnterpriseConfig")')],
    "posthog/settings/__init__.py": [(
        'if "ee.apps.EnterpriseConfig" in INSTALLED_APPS:\n    from ee.settings import *  # noqa: F401, F403',
        'if "ee.apps.EnterpriseConfig" in INSTALLED_APPS or "ee.ce.ReadyStackCEConfig" in INSTALLED_APPS:\n    from ee.settings import *  # noqa: F401, F403  (ReadyStack CE: the CE package\'s settings)')],
}
for path, pairs in edits.items():
    s = open(path).read()
    for old, new in pairs:
        assert s.count(old) == 1, f"{path}: upstream block moved: {old[:60]!r}"
        s = s.replace(old, new)
    open(path, "w").write(s)
print("ce-compat patch applied")
PY
