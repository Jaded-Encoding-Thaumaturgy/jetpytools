from __future__ import annotations

from itertools import chain, zip_longest
from typing import Iterable

from ..types import T0, T

__all__ = ["interleave_arr"]


def interleave_arr(arr0: Iterable[T], arr1: Iterable[T0], n: int = 2) -> Iterable[T | T0]:
    """
    Interleave two arrays of variable length.

    :param arr0:    First array to be interleaved.
    :param arr1:    Second array to be interleaved.
    :param n:       The number of elements from arr0 to include in the interleaved sequence
                    before including an element from arr1.

    :yield:         Elements from either arr0 or arr01.
    """
    if n == 1:
        yield from (x for x in chain.from_iterable(zip_longest(arr0, arr1)) if x is not None)

        return

    arr0_i, arr1_i = iter(arr0), iter(arr1)
    arr1_vals = arr0_vals = True

    while arr1_vals or arr0_vals:
        if arr0_vals:
            for _ in range(n):
                try:
                    yield next(arr0_i)
                except StopIteration:
                    arr0_vals = False

        if arr1_vals:
            try:
                yield next(arr1_i)
            except StopIteration:
                arr1_vals = False
