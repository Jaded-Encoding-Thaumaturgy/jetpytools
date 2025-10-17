from __future__ import annotations

from typing import Any, Callable, ParamSpec, Sequence, SupportsFloat, SupportsIndex, TypeVar

__all__ = [
    "F0",
    "F1",
    "F2",
    "P0",
    "P1",
    "P2",
    "R0",
    "R1",
    "R2",
    "T0",
    "T1",
    "T2",
    "ByteData",
    "F",
    "KwargsT",
    "Nb",
    "P",
    "R",
    "R0_co",
    "R1_co",
    "R_co",
    "R_contra",
    "SimpleByteData",
    "SimpleByteDataArray",
    "SingleOrArr",
    "SingleOrArrOpt",
    "SingleOrSeq",
    "SingleOrSeqOpt",
    "SoftRange",
    "SoftRangeN",
    "SoftRangesN",
    "StrictRange",
    "T",
    "T0_co",
    "T1_co",
    "T_co",
    "T_contra",
]

Nb = TypeVar("Nb", float, int)

T = TypeVar("T")
T0 = TypeVar("T0")
T1 = TypeVar("T1")
T2 = TypeVar("T2")

F = TypeVar("F", bound=Callable[..., Any])
F0 = TypeVar("F0", bound=Callable[..., Any])
F1 = TypeVar("F1", bound=Callable[..., Any])
F2 = TypeVar("F2", bound=Callable[..., Any])

P = ParamSpec("P")
P0 = ParamSpec("P0")
P1 = ParamSpec("P1")
P2 = ParamSpec("P2")

R = TypeVar("R")
R0 = TypeVar("R0")
R1 = TypeVar("R1")
R2 = TypeVar("R2")

T_co = TypeVar("T_co", covariant=True)
T0_co = TypeVar("T0_co", covariant=True)
T1_co = TypeVar("T1_co", covariant=True)

R_co = TypeVar("R_co", covariant=True)
R0_co = TypeVar("R0_co", covariant=True)
R1_co = TypeVar("R1_co", covariant=True)

T_contra = TypeVar("T_contra", contravariant=True)
R_contra = TypeVar("R_contra", contravariant=True)

type StrictRange = tuple[int, int]
type SoftRange = int | StrictRange | Sequence[int]

type SoftRangeN = int | tuple[int | None, int | None] | None

type SoftRangesN = Sequence[SoftRangeN]

type SingleOrArr[T] = T | list[T]
type SingleOrSeq[T] = T | Sequence[T]
type SingleOrArrOpt[T] = SingleOrArr[T] | None
type SingleOrSeqOpt[T] = SingleOrSeq[T] | None

type SimpleByteData = str | bytes | bytearray
type SimpleByteDataArray = SimpleByteData | Sequence[SimpleByteData]

type ByteData = SupportsFloat | SupportsIndex | SimpleByteData | memoryview

KwargsT = dict[str, Any]
