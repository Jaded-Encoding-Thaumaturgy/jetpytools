from __future__ import annotations

from jetpytools import fallback, iterate, kwargs_fallback


def test_iterate() -> None:
    assert iterate(5, lambda x: x * 2, 2) == 20


def test_fallback() -> None:
    assert fallback(5, 6) == 5
    assert fallback(None, 6) == 6


def test_kwargs_fallback() -> None:
    kwargs = {"overlap": 1, "search": 2, "block_size": 4, "sad_mode": 8, "motion": 12, "thSAD": 16}

    assert kwargs_fallback(5, (kwargs, "block_size"), 8) == 5
    assert kwargs_fallback(None, (kwargs, "block_size"), 8) == 4
    assert kwargs_fallback(None, ({}, "block_size"), 8) == 8
