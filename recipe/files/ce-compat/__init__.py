# ReadyStack CE compatibility package for PostHog -- MIT licence, written by ReadyStack. It is NOT PostHog's ee/
# directory (PostHog Enterprise licence), which this build removes. PostHog's MIT code imports names from `ee.*`
# and declares models under the Django app label "ee"; this package provides that app label, the migration nodes the
# MIT migrations depend on, and, for every other `ee.*` name, a placeholder that marks the Enterprise feature absent.
import importlib.abc
import importlib.machinery
import re
import sys
import types

_REAL = {"ee", "ee.apps", "ee.ce", "ee.settings", "ee.migrations"}
_ABSENT_MODULES = {"ee.urls"}  # ImportError, so PostHog's own "no EE" branches run


class EnterpriseFeatureUnavailable(RuntimeError):
    """Raised when code reaches an Enterprise-only feature that this Community Edition build does not include."""


def _absent_call(qualname):
    def call(*args, **kwargs):
        # used as a decorator (@absent or @absent(...)): return the decorated object unchanged
        if len(args) == 1 and not kwargs and (callable(args[0]) or isinstance(args[0], type)):
            return args[0]
        return _Absent(qualname + "()")
    return call


class _Absent:
    __slots__ = ("_qn",)

    def __init__(self, qn):
        object.__setattr__(self, "_qn", qn)

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return _make(f"{self._qn}.{name}", name)

    def __call__(self, *a, **k):
        return _absent_call(self._qn)(*a, **k)

    def __bool__(self):
        return False

    def __iter__(self):
        return iter(())

    def __len__(self):
        return 0

    def __contains__(self, item):
        return False

    def __getitem__(self, item):
        return self

    def __str__(self):
        return ""

    def __repr__(self):
        return f"<CE: {self._qn} not in this build>"

    def __mro_entries__(self, bases):
        return (_make_class(self._qn.rsplit(".", 1)[-1], self._qn),)


class _AbsentMeta(type):
    def __getattr__(cls, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return _make(f"{cls.__qualname__}.{name}", name)

    def __getitem__(cls, item):
        return cls

    def __get_pydantic_core_schema__(cls, source, handler):
        from pydantic_core import core_schema
        return core_schema.any_schema()


def _make_class(name, qn):
    def _init(self, *a, **k):
        pass
    return _AbsentMeta(name, (), {"__qualname__": name, "__module__": qn.rsplit(".", 1)[0], "__init__": _init,
                                  "__getattr__": lambda self, n: _make(f"{qn}().{n}", n)})


class _AbsentConst(str):
    """An Enterprise constant (UPPER_CASE): an empty string that also tolerates attribute and item access."""
    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return _AbsentConst("")

    def __getitem__(self, item):
        return self

    def __call__(self, *a, **k):
        return self


def _make(qn, name):
    if name.isupper() or re.fullmatch(r"[A-Z0-9_]+", name):
        return _AbsentConst("")
    if re.search(r"(Error|Exception)$", name):
        return type(name, (EnterpriseFeatureUnavailable,), {"__module__": qn.rsplit(".", 1)[0]})
    if name.endswith("ViewSet"):
        # an Enterprise API: a viewset with no actions, so routers register no routes for it
        from rest_framework import viewsets
        return type(name, (viewsets.ViewSet,), {"__module__": qn.rsplit(".", 1)[0], "lookup_field": "pk",
                                                "__doc__": "Enterprise API not included in this CE build."})
    if name.endswith("Serializer"):
        from rest_framework import serializers
        return type(name, (serializers.Serializer,), {"__module__": qn.rsplit(".", 1)[0]})
    if name[:1].isupper() and not name.isupper():
        return _make_class(name, qn)
    return _Absent(qn)


class _AbsentModule(types.ModuleType):
    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        v = _make(f"{self.__name__}.{name}", name)
        setattr(self, name, v)
        return v


class _Finder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, fullname, path=None, target=None):
        if not fullname.startswith("ee.") or fullname in _REAL or fullname.startswith("ee.migrations"):
            return None
        if fullname in _ABSENT_MODULES:
            return None
        return importlib.machinery.ModuleSpec(fullname, self, is_package=True)

    def create_module(self, spec):
        m = _AbsentModule(spec.name)
        m.__path__ = []
        return m

    def exec_module(self, module):
        pass


if not any(isinstance(f, _Finder) for f in sys.meta_path):
    sys.meta_path.append(_Finder())
