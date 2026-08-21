from pathlib import Path

import pytest

from romeo.doctor.identity import (
    UnitIdentityError,
    fingerprint_unit_identifier,
    is_unit_fingerprint,
    read_raspberry_unit_identifier,
)


def test_device_tree_identifier_is_preferred_and_hashed(tmp_path: Path) -> None:
    device_tree = tmp_path / "serial-number"
    cpuinfo = tmp_path / "cpuinfo"
    device_tree.write_bytes(b"raw-device-tree-serial\x00")
    cpuinfo.write_text("Serial : fallback-serial\n", encoding="ascii")

    raw = read_raspberry_unit_identifier(
        device_tree_paths=(device_tree,), cpuinfo_path=cpuinfo
    )
    fingerprint = fingerprint_unit_identifier(raw)

    assert raw == "raw-device-tree-serial"
    assert is_unit_fingerprint(fingerprint)
    assert "raw-device-tree-serial" not in fingerprint


def test_cpuinfo_serial_is_an_older_raspberry_fallback(tmp_path: Path) -> None:
    cpuinfo = tmp_path / "cpuinfo"
    cpuinfo.write_text("Model : Raspberry Pi\nSerial : fallback-serial\n", encoding="ascii")

    assert read_raspberry_unit_identifier(
        device_tree_paths=(tmp_path / "missing",), cpuinfo_path=cpuinfo
    ) == "fallback-serial"


def test_identifier_unavailable_is_explicit(tmp_path: Path) -> None:
    with pytest.raises(UnitIdentityError, match="unavailable"):
        read_raspberry_unit_identifier(
            device_tree_paths=(tmp_path / "missing",),
            cpuinfo_path=tmp_path / "missing-cpuinfo",
        )


def test_cpuinfo_serial_is_not_used_on_a_non_raspberry_host(tmp_path: Path) -> None:
    cpuinfo = tmp_path / "cpuinfo"
    cpuinfo.write_text("Model : Generic ARM board\nSerial : unrelated-serial\n", encoding="ascii")

    with pytest.raises(UnitIdentityError, match="unavailable"):
        read_raspberry_unit_identifier(
            device_tree_paths=(tmp_path / "missing",), cpuinfo_path=cpuinfo
        )
