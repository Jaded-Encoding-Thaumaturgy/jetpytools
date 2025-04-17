from __future__ import annotations

from jetpytools import fallback, iterate


def test_iterate() -> None:
    assert iterate(5, lambda x: x * 2, 2) == 20


def test_fallback() -> None:
    assert fallback(5, 6) == 5
    assert fallback(None, 6) == 6
