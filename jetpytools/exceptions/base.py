from __future__ import annotations

import sys
from contextlib import AbstractContextManager
from copy import deepcopy
from types import TracebackType
from typing import TYPE_CHECKING, Any

from typing_extensions import Self

from ..types import MISSING, FuncExcept, MissingT, SupportsString

__all__ = [
    "CustomError",
    "CustomIndexError",
    "CustomKeyError",
    "CustomNotImplementedError",
    "CustomOverflowError",
    "CustomPermissionError",
    "CustomRuntimeError",
    "CustomTypeError",
    "CustomValueError",
]


if TYPE_CHECKING:

    class ExceptionError(Exception):
        __name__: str
        __qualname__: str
else:
    ExceptionError = Exception


class CustomErrorMeta(type):
    """Custom base exception meta class."""

    def __new__[MetaSelf: CustomErrorMeta](cls: type[MetaSelf], *args: Any) -> MetaSelf:
        return CustomErrorMeta.setup_exception(super().__new__(cls, *args))

    @staticmethod
    def setup_exception[MetaSelf: CustomErrorMeta](
        exception: MetaSelf, override: str | ExceptionError | None = None
    ) -> MetaSelf:
        """
        Setup an exception for later use in CustomError.

        :param exception:   Exception to update.
        :param override:    Optional name or exception from which get the override values.

        :return:            Set up exception.
        """

        if override:
            if isinstance(override, str):
                over_name = over_qual = override
            else:
                over_name, over_qual = override.__name__, override.__qualname__

            if over_name.startswith("Custom"):
                exception.__name__ = over_name
            else:
                exception.__name__ = f"Custom{over_name}"

            exception.__qualname__ = over_qual

        if exception.__qualname__.startswith("Custom"):
            exception.__qualname__ = exception.__qualname__[6:]

        if sys.stdout and sys.stdout.isatty():
            exception.__qualname__ = f"\033[0;31;1m{exception.__qualname__}\033[0m"

        exception.__module__ = Exception.__module__

        return exception


class CustomError(ExceptionError, metaclass=CustomErrorMeta):
    """Custom base exception class."""

    def __init__(
        self, message: SupportsString | None = None, func: FuncExcept | None = None, reason: Any = None, **kwargs: Any
    ) -> None:
        """
        Instantiate a new exception with pretty printing and more.

        :param message: Message of the error.
        :param func:    Function this exception was raised from.
        :param reason:  Reason of the exception. For example, an optional parameter.
        """

        self.message = message
        self.func = func
        self.reason = reason
        self.kwargs = kwargs

        super().__init__(message)

    def __call__(
        self,
        message: SupportsString | None | MissingT = MISSING,
        func: FuncExcept | None | MissingT = MISSING,
        reason: SupportsString | FuncExcept | None | MissingT = MISSING,
        **kwargs: Any,
    ) -> Self:
        """
        Copy an existing exception with defaults and instantiate a new one.

        :param message: Message of the error.
        :param func:    Function this exception was raised from.
        :param reason:  Reason of the exception. For example, an optional parameter.
        """

        err = deepcopy(self)

        if message is not MISSING:
            err.message = message

        if func is not MISSING:
            err.func = func

        if reason is not MISSING:
            err.reason = reason

        err.kwargs |= kwargs

        return err

    def __str__(self) -> str:
        from ..functions import norm_display_name, norm_func_name

        message = self.message

        if not message:
            message = "An error occurred!"

        if self.func:
            func_header = norm_func_name(self.func).strip()

            if sys.stdout and sys.stdout.isatty():
                func_header = f"\033[0;36m{func_header}\033[0m"

            func_header = f"({func_header}) "
        else:
            func_header = ""

        if self.kwargs:
            self.kwargs = {key: norm_display_name(value) for key, value in self.kwargs.items()}

        if self.reason:
            reason = self.reason = norm_display_name(self.reason)

            if reason:
                if not isinstance(self.reason, dict):
                    reason = f"({reason})"

                if sys.stdout and sys.stdout.isatty():
                    reason = f"\033[0;33m{reason}\033[0m"
                reason = f" {reason}"
        else:
            reason = ""

        out = f"{func_header}{self.message!s}{reason}".format(**self.kwargs).strip()

        return out

    @classmethod
    def catch(cls) -> CatchError[Self]:
        """
        Create a context manager that catches exceptions of this class type.

        Returns:
            CatchError[Self]: A context manager that will catch and store exceptions of type `cls`
                when used in a `with` block.
        """
        return CatchError(cls)


class CatchError[CustomErrorT: CustomError](AbstractContextManager["CatchError[CustomErrorT]"]):
    """
    Context manager for catching a specific exception type.
    """

    error: CustomErrorT | None
    """The caught exception instance, if any."""
    tb: TracebackType | None
    """The traceback object associated with the caught exception."""

    def __init__(self, error: type[CustomErrorT]) -> None:
        self.error = None
        self.tb = None
        self._to_catch_error = error

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        if isinstance(exc_value, self._to_catch_error):
            self.error = exc_value
            self.tb = traceback
            return True

        return None


class CustomValueError(CustomError, ValueError):
    """Thrown when a specified value is invalid."""


class CustomIndexError(CustomError, IndexError):
    """Thrown when an index or generic numeric value is out of bound."""


class CustomOverflowError(CustomError, OverflowError):
    """Thrown when a value is out of range. e.g. temporal radius too big."""


class CustomKeyError(CustomError, KeyError):
    """Thrown when trying to access an non-existent key."""


class CustomTypeError(CustomError, TypeError):
    """Thrown when a passed argument is of wrong type."""


class CustomRuntimeError(CustomError, RuntimeError):
    """Thrown when a runtime error occurs."""


class CustomNotImplementedError(CustomError, NotImplementedError):
    """Thrown when you encounter a yet not implemented branch of code."""


class CustomPermissionError(CustomError, PermissionError):
    """Thrown when the user can't perform an action."""
