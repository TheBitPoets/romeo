"""Opt-in physical preflight; never moves motors or servo."""

import os

import pytest

from romeo.doctor.checks import run_preflight
from romeo.doctor.config import default_config_path

pytestmark = pytest.mark.hardware


@pytest.mark.skipif(
    os.environ.get("ROMEO_HARDWARE_TEST") != "1",
    reason="set ROMEO_HARDWARE_TEST=1 on the supervised Raspberry Pi",
)
def test_physical_passive_preflight_is_ready() -> None:
    report = run_preflight(default_config_path())

    assert report.ready, report.to_dict()
