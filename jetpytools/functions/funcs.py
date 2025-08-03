from __future__ import annotations

from inspect import signature
from typing import Any, Callable, Concatenate, overload

from ..exceptions import CustomRuntimeError, CustomValueError
from ..types import MISSING, KwargsT, MissingT, P, R, T

__all__ = ["fallback", "filter_kwargs", "iterate", "kwargs_fallback"]


def iterate(
    base: T, function: Callable[Concatenate[T | R, P], R], count: int, *args: P.args, **kwargs: P.kwargs
) -> T | R:
    """
    Execute a given function over the base value multiple times.

    Different from regular iteration functions is that you do not need to pass a partial object.
    This function accepts *args and **kwargs. These will be passed on to the given function.

    Examples:

    >>> iterate(5, lambda x: x * 2, 2)
        20

    :param base:        Base value, etc. to iterate over.
    :param function:    Function to iterate over the base.
    :param count:       Number of times to execute function.
    :param *args:       Positional arguments to pass to the given function.
    :param **kwargs:    Keyword arguments to pass to the given function.

    :return:            Value, etc. with the given function run over it
                        *n* amount of times based on the given count.
    """

    if count <= 0:
        return base

    result: T | R = base

    for _ in range(count):
        result = function(result, *args, **kwargs)

    return result


fallback_missing = object()


@overload
def fallback(value: T | None, fallback: T, /) -> T: ...


@overload
def fallback(value: T | None, fallback0: T | None, default: T, /) -> T: ...


@overload
def fallback(value: T | None, fallback0: T | None, fallback1: T | None, default: T, /) -> T: ...


@overload
def fallback(value: T | None, *fallbacks: T | None) -> T | MissingT: ...


@overload
def fallback(value: T | None, *fallbacks: T | None, default: T) -> T: ...


def fallback(value: T | None, *fallbacks: T | None, default: Any | T = fallback_missing) -> T | MissingT:
    """
    Utility function that returns a value or a fallback if the value is None.

    Example:

    .. code-block:: python

        >>> fallback(5, 6)
        5
        >>> fallback(None, 6)
        6

    :param value:               Input value to evaluate. Can be None.
    :param fallback_value:      Value to return if the input value is None.

    :return:                    Input value or fallback value if input value is None.
    """

    if value is not None:
        return value

    for fallback in fallbacks:
        if fallback is not None:
            return fallback

    if default is not fallback_missing:
        return default
    elif len(fallbacks) > 3:
        return MISSING

    raise CustomRuntimeError("You need to specify a default/fallback value!")


@overload
def kwargs_fallback(input_value: T | None, kwargs: tuple[KwargsT, str], fallback: T) -> T: ...


@overload
def kwargs_fallback(input_value: T | None, kwargs: tuple[KwargsT, str], fallback0: T | None, default: T) -> T: ...


@overload
def kwargs_fallback(
    input_value: T | None, kwargs: tuple[KwargsT, str], fallback0: T | None, fallback1: T | None, default: T
) -> T: ...


@overload
def kwargs_fallback(input_value: T | None, kwargs: tuple[KwargsT, str], *fallbacks: T | None) -> T | MissingT: ...


@overload
def kwargs_fallback(input_value: T | None, kwargs: tuple[KwargsT, str], *fallbacks: T | None, default: T) -> T: ...


def kwargs_fallback(  # type: ignore
    value: T | None,
    kwargs: tuple[KwargsT, str],
    *fallbacks: T | None,
    default: T = fallback_missing,  # type: ignore
) -> T | MissingT:
    """Utility function to return a fallback value from kwargs if value was not found or is None."""

    return fallback(value, kwargs[0].get(kwargs[1], None), *fallbacks, default=default)


@overload
def filter_kwargs(func: Callable[..., Any], kwargs: dict[str, Any]) -> dict[str, Any]: ...


@overload
def filter_kwargs(func: Callable[..., Any], **kwargs: Any) -> dict[str, Any]: ...


def filter_kwargs(func: Callable[..., Any], kwargs: dict[str, Any] | None = None, **kw: Any) -> dict[str, Any]:
    """
    Filter kwargs to only include parameters that match the callable's signature, ignoring **kwargs.

    Examples:

        >>> def my_func(a: int, b: str, c: bool = True):
        ...     return a, b, c
        >>> filter_kwargs(my_func, a=1, b="hello", c=False, d="extra")
        {'a': 1, 'b': 'hello', 'c': False}
        >>> filter_kwargs(my_func, {"a": 1, "b": "hello", "c": False, "d": "extra"})
        {'a': 1, 'b': 'hello', 'c': False}

    :param func:        The callable to filter kwargs for.
    :param kwargs:      Dictionary of keyword arguments to filter.
    :param **kw:        Keyword arguments to filter (used when kwargs is None).

    :return:            A dictionary containing only the kwargs that match the callable's parameters.
    """

    if not (filtered_kwargs := fallback(kwargs, kw)):
        return {}

    try:
        sig = signature(func)
    except Exception as e:
        raise CustomValueError(e.args[0], filter_kwargs, func) from e

    param_names = {name for name, param in sig.parameters.items() if param.kind != param.VAR_KEYWORD}

    return {name: value for name, value in filtered_kwargs.items() if name in param_names}
