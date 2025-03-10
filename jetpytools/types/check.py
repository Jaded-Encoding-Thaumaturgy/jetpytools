from typing import Any, Sequence

from typing_extensions import TypeIs

from .builtins import SoftRange, SoftRangeN, SoftRangesN, StrictRange

__all__ = [
    "is_strict_range", "is_soft_range", "is_soft_range_n", "is_soft_ranges_n"
]


def is_strict_range(val: Any) -> TypeIs[StrictRange]:
    return isinstance(val, tuple) and len(val) == 2 and all(isinstance(x, int) for x in val)


def is_soft_range(val: Any) -> TypeIs[SoftRange]:
    return isinstance(val, int) or is_strict_range(val) or (
        isinstance(val, Sequence) and all(isinstance(x, int) for x in val)
    )


def is_soft_range_n(val: Any) -> TypeIs[SoftRangeN]:
    return (
        isinstance(val, int)
        or (isinstance(val, tuple) and len(val) == 2 and all(isinstance(x, int) or x is None for x in val))
        or val is None
    )


def is_soft_ranges_n(val: Any) -> TypeIs[SoftRangesN]:
    return (
        isinstance(val, Sequence)
        and all(is_soft_range_n(x) for x in val)
    )
