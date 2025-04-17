from __future__ import annotations

from jetpytools import normalize_ranges


def test_normalize_ranges() -> None:
    assert normalize_ranges((None, None), end=1000) == [(0, 999)]
    assert normalize_ranges((24, -24), end=1000) == [(24, 975)]
    assert normalize_ranges([(24, 100), (80, 150)], end=1000) == [(24, 150)]
