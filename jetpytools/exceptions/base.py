from __future__ import annotations

import sys

from copy import deepcopy
from typing import TYPE_CHECKING, Any, TypeVar

from typing_extensions import Self

from ..types import MISSING, FuncExceptT, SupportsString, MissingT

__all__ = [
    'CustomError',

    'CustomValueError',
    'CustomIndexError',
    'CustomOverflowError',
    'CustomKeyError',
    'CustomTypeError',
    'CustomRuntimeError',
    'CustomNotImplementedError',
    'CustomPermissionError'
]


if TYPE_CHECKING:
    class ExceptionT(Exception):
        __name__: str
        __qualname__: str
        ...
else:
    ExceptionT = Exception


class CustomErrorMeta(type):
    """Custom base exception meta class."""

    def __new__(cls: type[SelfCErrorMeta], *args: Any) -> SelfCErrorMeta:
        return CustomErrorMeta.setup_exception(type.__new__(cls, *args))  # type: ignore

    @staticmethod
    def setup_exception(exception: SelfCErrorMeta, override: str | ExceptionT | None = None) -> SelfCErrorMeta:
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

            if over_name.startswith('Custom'):
                exception.__name__ = over_name
            else:
                exception.__name__ = f'Custom{over_name}'

            exception.__qualname__ = over_qual

        if exception.__qualname__.startswith('Custom'):
            exception.__qualname__ = exception.__qualname__[6:]

        if sys.stdout and sys.stdout.isatty():
            exception.__qualname__ = f'\033[0;31;1m{exception.__qualname__}\033[0m'

        exception.__module__ = Exception.__module__

        return exception


SelfCErrorMeta = TypeVar('SelfCErrorMeta', bound=CustomErrorMeta)


class CustomError(ExceptionT, metaclass=CustomErrorMeta):
    """Custom base exception class."""

    def __init__(
        self, message: SupportsString | None = None, func: FuncExceptT | None = None, reason: Any = None, **kwargs: Any
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

    def __class_getitem__(cls, exception: str | type[ExceptionT] | ExceptionT) -> CustomError:
        from warnings import warn

        warn("Custom error is not subscriptable anymore. Don't use it", DeprecationWarning)

        return cls()

    def __call__(
        self,
        message: SupportsString | None | MissingT = MISSING,
        func: FuncExceptT | None | MissingT = MISSING,
        reason: SupportsString | FuncExceptT | None | MissingT = MISSING,
        **kwargs: Any
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
            message = 'An error occurred!'

        if self.func:
            func_header = norm_func_name(self.func).strip()

            if sys.stdout and sys.stdout.isatty():
                func_header = f'\033[0;36m{func_header}\033[0m'

            func_header = f'({func_header}) '
        else:
            func_header = ''

        if self.kwargs:
            self.kwargs = {
                key: norm_display_name(value) for key, value in self.kwargs.items()
            }

        if self.reason:
            reason = self.reason = norm_display_name(self.reason)

            if reason:
                if not isinstance(self.reason, dict):
                    reason = f'({reason})'

                if sys.stdout and sys.stdout.isatty():
                    reason = f'\033[0;33m{reason}\033[0m'
                reason = f' {reason}'
        else:
            reason = ''

        return f'{func_header}{self.message!s}{reason}'.format(**self.kwargs).strip()


SelfError = TypeVar('SelfError', bound=CustomError)


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
