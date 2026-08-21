from __future__ import annotations

import runpy
import time
from pathlib import Path

import pytest

from romeo import easy

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("name", ["first_move.py", "square.py"])
def test_documented_examples_run_on_default_mock(monkeypatch, name: str) -> None:
    monkeypatch.setattr(time, "sleep", lambda _seconds: None)
    try:
        runpy.run_path(str(ROOT / "examples" / name), run_name="__main__")
    finally:
        easy.close()
