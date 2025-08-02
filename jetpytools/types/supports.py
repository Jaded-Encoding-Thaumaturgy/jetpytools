from __future__ import annotations

from abc import abstractmethod
from typing import (
    Any,
    Callable,
    Iterable,
    Protocol,
    SupportsFloat,
    SupportsIndex,
    TypeAlias,
    TypeVar,
    overload,
    runtime_checkable,
)

from .builtins import T0, T1, T2, T_co, T_contra

__all__ = [
    "ComparatorFunc",
    "SupportsAdd",
    "SupportsAllComparisons",
    "SupportsDunderGE",
    "SupportsDunderGT",
    "SupportsDunderLE",
    "SupportsDunderLT",
    "SupportsFloatOrIndex",
    "SupportsIndexing",
    "SupportsKeysAndGetItem",
    "SupportsRAdd",
    "SupportsRichComparison",
    "SupportsRichComparisonT",
    "SupportsString",
    "SupportsSumNoDefaultT",
    "SupportsTrunc",
]


_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)


@runtime_checkable
class SupportsAdd(Protocol[T_contra, T_co]):
    def __add__(self, x: T_contra, /) -> T_co: ...


@runtime_checkable
class SupportsRAdd(Protocol[T_contra, T_co]):
    def __radd__(self, x: T_contra, /) -> T_co: ...


class _SupportsSumWithNoDefaultGiven(SupportsAdd[Any, Any], SupportsRAdd[int, Any], Protocol): ...


SupportsSumNoDefaultT = TypeVar("SupportsSumNoDefaultT", bound=_SupportsSumWithNoDefaultGiven)


@runtime_checkable
class SupportsTrunc(Protocol):
    def __trunc__(self) -> int: ...


@runtime_checkable
class SupportsString(Protocol):
    @abstractmethod
    def __str__(self) -> str: ...


@runtime_checkable
class SupportsDunderLT(Protocol[T_contra]):
    def __lt__(self, other: T_contra) -> bool: ...


@runtime_checkable
class SupportsDunderGT(Protocol[T_contra]):
    def __gt__(self, other: T_contra) -> bool: ...


@runtime_checkable
class SupportsDunderLE(Protocol[T_contra]):
    def __le__(self, other: T_contra) -> bool: ...


@runtime_checkable
class SupportsDunderGE(Protocol[T_contra]):
    def __ge__(self, other: T_contra) -> bool: ...


@runtime_checkable
class SupportsAllComparisons(
    SupportsDunderLT[Any], SupportsDunderGT[Any], SupportsDunderLE[Any], SupportsDunderGE[Any], Protocol
): ...


SupportsRichComparison: TypeAlias = SupportsDunderLT[Any] | SupportsDunderGT[Any]
SupportsRichComparisonT = TypeVar("SupportsRichComparisonT", bound=SupportsRichComparison)


class ComparatorFunc(Protocol):
    @overload
    def __call__(
        self,
        arg1: SupportsRichComparisonT,
        arg2: SupportsRichComparisonT,
        /,
        *args: SupportsRichComparisonT,
        key: None = ...,
    ) -> SupportsRichComparisonT: ...

    @overload
    def __call__(self, arg1: T0, arg2: T0, /, *_args: T0, key: Callable[[T0], SupportsRichComparison]) -> T0: ...

    @overload
    def __call__(
        self, iterable: Iterable[SupportsRichComparisonT], /, *, key: None = ...
    ) -> SupportsRichComparisonT: ...

    @overload
    def __call__(self, iterable: Iterable[T0], /, *, key: Callable[[T0], SupportsRichComparison]) -> T0: ...

    @overload
    def __call__(
        self, iterable: Iterable[SupportsRichComparisonT], /, *, key: None = ..., default: T0
    ) -> SupportsRichComparisonT | T0: ...

    @overload
    def __call__(
        self, iterable: Iterable[T1], /, *, key: Callable[[T1], SupportsRichComparison], default: T2
    ) -> T1 | T2: ...


class SupportsIndexing(Protocol[_VT_co]):
    def __getitem__(self, k: int) -> _VT_co: ...


class SupportsKeysAndGetItem(Protocol[_KT, _VT_co]):
    def keys(self) -> Iterable[_KT]: ...

    def __getitem__(self, k: _KT) -> _VT_co: ...


SupportsFloatOrIndex: TypeAlias = SupportsFloat | SupportsIndex
