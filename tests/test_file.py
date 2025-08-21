from __future__ import annotations

from jetpytools import get_script_path


def test_get_script_path() -> None:
    script_path = get_script_path()
    assert script_path is not None
    assert script_path.exists()
