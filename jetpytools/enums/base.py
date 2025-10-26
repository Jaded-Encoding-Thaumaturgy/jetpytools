from __future__ import annotations

from abc import ABCMeta
from enum import Enum, EnumMeta, ReprEnum
from enum import property as enum_property
from typing import TYPE_CHECKING, Any, Self

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


class CustomIntEnum(int, CustomEnum, ReprEnum):
    """Base class for custom int enums."""

    if TYPE_CHECKING:
        _value_: int

        @enum_property
        def value(self) -> int: ...


class CustomStrEnum(str, CustomEnum, ReprEnum):
    """Base class for custom str enums."""

    if TYPE_CHECKING:
        _value_: str

        @enum_property
        def value(self) -> str: ...
