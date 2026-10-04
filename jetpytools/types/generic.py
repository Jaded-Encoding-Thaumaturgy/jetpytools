from __future__ import annotations

from collections.abc import Callable
from typing import Any

from typing_extensions import Sentinel as sentinel  # noqa: N813

from .builtins import SingleOrArr, SingleOrArrOpt
from .supports import SupportsString

__all__ = ["MISSING", "DataType", "FuncExcept", "FuncExceptT", "MissingT", "PassthroughC", "StrArr", "StrArrOpt"]


MISSING = sentinel("MISSING")
MissingT = MISSING


type DataType = str | bytes | bytearray | SupportsString

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

type PassthroughC[F: Callable[..., Any]] = Callable[[F], F]
