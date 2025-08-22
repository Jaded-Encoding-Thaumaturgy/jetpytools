from __future__ import annotations

from typing import Any, Callable, TypeAlias, Union

from .builtins import F, SingleOrArr, SingleOrArrOpt
from .supports import SupportsString

__all__ = ["MISSING", "DataType", "FuncExcept", "MissingT", "PassthroughC", "StrArr", "StrArrOpt"]


class _MissingType:
    __slots__ = ()

    def __repr__(self) -> str:
        return "<MISSING>"


MissingT: TypeAlias = _MissingType
MISSING = _MissingType()

DataType = Union[str, bytes, bytearray, SupportsString]

FuncExcept = str | Callable[..., Any] | tuple[Callable[..., Any] | str, str]
"""
This type is used in specific functions that can throw an exception.
```
def can_throw(..., *, func: FuncExcept) -> None:
    ...
    if some_error:
        raise CustomValueError('Some error occurred!!', func)

def some_func() -> None:
    ...
    can_throw(..., func=some_func)
```
If an error occurs, this will print a clear error ->\n
``ValueError: (some_func) Some error occurred!!``
"""

FuncExceptT = FuncExcept

StrArr = SingleOrArr[SupportsString]
StrArrOpt = SingleOrArrOpt[SupportsString]

PassthroughC = Callable[[F], F]
