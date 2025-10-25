from __future__ import annotations

from abc import ABCMeta
from enum import Enum, EnumMeta
from typing import Any, Self

from ..exceptions import NotFoundEnumValueError
from ..types import FuncExcept

__all__ = ["CustomEnum", "CustomIntEnum", "CustomStrEnum", "EnumABCMeta"]


class EnumABCMeta(EnumMeta, ABCMeta):
    """Metaclass combining EnumMeta and ABCMeta to support abstract enumerations."""


class CustomEnum(Enum):
    """Base class for custom enums."""

    @classmethod
    def from_param(cls, value: Any, func_except: FuncExcept | None = None) -> Self:
        """
        Return the enum value from a parameter.

        :param value:               Value to instantiate the enum class.
        :param func_except:         Exception function.

        :return:                    Enum value.

        :raises NotFoundEnumValue:   Variable not found in the given enum.
        """
        func_except = func_except or cls.from_param

        try:
            return cls(value)
        except (ValueError, TypeError):
            pass

        if isinstance(func_except, tuple):
            func_name, var_name = func_except
        else:
            func_name, var_name = func_except, repr(cls)

        raise NotFoundEnumValueError(
            'The given value for "{var_name}" argument must be a valid {enum_name}, not "{value}"!\n'
            "Valid values are: [{readable_enum}].",
            func_name,
            var_name=var_name,
            enum_name=cls,
            value=value,
            readable_enum=(f"{name} ({value!r})" for name, value in cls.__members__.items()),
            reason=value,
        ) from None


class CustomIntEnum(int, CustomEnum):
    """Base class for custom int enums."""

    _value_: int


class CustomStrEnum(str, CustomEnum):
    """Base class for custom str enums."""

    _value_: str
