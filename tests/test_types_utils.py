from inspect import Signature
from typing import Any

from jetpytools import inject_self
from jetpytools.types.utils import _self_objects_cache


def test_inject_self_instance_and_class() -> None:
    class A:
        def __init__(self) -> None:
            self.value = 42

        @inject_self
        def foo(self) -> int:
            return self.value

    a = A()
    # When called on instance, normal method behavior
    assert a.foo() == 42

    # When called on class, should auto-instantiate and inject
    assert A.foo() == 42


def test_inject_self_cached_reuses_instance() -> None:
    _self_objects_cache.clear()

    class B:
        def __init__(self) -> None:
            self.created = True

        @inject_self.cached
        def id(self) -> int:
            return id(self)

    first_id = B.id()
    second_id = B.id()

    assert first_id == second_id
    assert B in _self_objects_cache or any(isinstance(v, B) for v in _self_objects_cache.values())


def test_inject_self_cached_property_variant() -> None:
    _self_objects_cache.clear()

    class C:
        counter = 0

        def __init__(self) -> None:
            C.counter += 1

        @inject_self.cached.property
        def prop(self) -> int:
            return self.counter

    # Should instantiate once
    assert C.prop == 1
    assert C.prop == 1
    assert len(_self_objects_cache) == 1


def test_inject_self_init_kwargs_forwards_args() -> None:
    class D:
        def __init__(self, x: int = 10, y: int = 5) -> None:
            self.x = x
            self.y = y

        @inject_self.init_kwargs
        def add(self, *, x: int | None = None, y: int | None = None) -> int:
            return self.x + self.y

    # kwargs forwarded to constructor
    result = D.add(x=3, y=7)
    assert result == 10  # 3 + 7 in constructor, not function
    assert isinstance(result, int)


def test_inject_self_init_kwargs_clean_removes_forwarded() -> None:
    class E:
        def __init__(self, x: int = 0, y: int = 0) -> None:
            self.x = x
            self.y = y

        @inject_self.init_kwargs.clean
        def diff(self, *, x: int | None = None, y: int | None = None, z: int | None = 0) -> tuple[Any, ...]:
            # x and y should have been removed from kwargs
            return (x, y, z, self.x, self.y)

    result = E.diff(x=4, y=6, z=9)
    # x and y removed from kwargs, only z remains in call
    assert result == (None, None, 9, 4, 6)


def test_inject_self_with_args_factory() -> None:
    class F:
        def __init__(self, val: Any) -> None:
            self.val = val

        @inject_self.with_args(123)
        def get_val(self) -> Any:
            return self.val

    # Automatically constructs with val=123
    assert F.get_val() == 123


def test_inject_self_property_auto_call() -> None:
    class G:
        def __init__(self) -> None:
            self.n = 7

        @inject_self.property
        def prop(self) -> int:
            return self.n

    g = G()
    assert g.prop == 7
    assert G.prop == 7


def test_inject_self_metaclass_behavior() -> None:
    # Should allow issubclass checks between all inject_self variants
    assert issubclass(inject_self.cached, inject_self)
    assert issubclass(inject_self.init_kwargs, inject_self)
    assert issubclass(inject_self.init_kwargs.clean, inject_self.init_kwargs)

    # Also instance checks using metaclass dispatch
    c = inject_self.cached(lambda self: None)
    assert isinstance(c, inject_self)  # type: ignore[unreachable]


def test_signature_caching_and_func_property() -> None:
    class H:
        @inject_self
        def foo(self, x: Any) -> Any:
            return x

    wrapped = H.__dict__["foo"]
    sig = wrapped.__signature__
    assert isinstance(sig, Signature)
    assert "x" in sig.parameters

    assert callable(wrapped.__func__)
