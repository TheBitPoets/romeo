import json
from pathlib import Path

import pytest

from romeo.doctor import (
    CalibrationValues,
    CommissioningRecord,
    DoctorConfig,
    DoctorConfigError,
    DoctorConfigInvalidError,
    DoctorConfigVersionError,
    default_config_path,
    load_config,
    save_config,
)


def test_default_config_path_honours_explicit_and_xdg_locations() -> None:
    assert default_config_path({"ROMEO_DOCTOR_CONFIG": "/tmp/unit.json"}) == Path(
        "/tmp/unit.json"
    )
    assert default_config_path({"XDG_CONFIG_HOME": "/tmp/config"}) == Path(
        "/tmp/config/romeo/hardware.json"
    )


def test_missing_config_loads_safe_uncommissioned_defaults(tmp_path: Path) -> None:
    config = load_config(tmp_path / "missing.json")

    assert config.unit_calibration is None
    assert config.commissioning.status == "not_commissioned"


def test_save_and_load_round_trip_creates_parent_directory(tmp_path: Path) -> None:
    path = tmp_path / "romeo" / "doctor.json"
    expected = DoctorConfig(
        unit_calibration=CalibrationValues(
            left_inverted=True,
            right_trim=-0.08,
            speed_limit=0.35,
            pan_min=25,
            pan_max=155,
            tilt_min=30,
            tilt_max=145,
            watchdog_timeout=0.5,
        ),
        commissioning=CommissioningRecord(
            status="commissioned",
            timestamp="2026-08-21T12:00:00Z",
            package_version="0.1.0",
        ),
    )

    save_config(path, expected)

    assert load_config(path) == expected
    assert json.loads(path.read_text(encoding="utf-8"))["schema_version"].endswith(".v1")
    assert not list(path.parent.glob("*.tmp"))


def test_corrupt_json_is_reported_without_falling_back_to_defaults(tmp_path: Path) -> None:
    path = tmp_path / "doctor.json"
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(DoctorConfigInvalidError, match="invalid JSON"):
        load_config(path)


def test_version_mismatch_has_a_specific_error(tmp_path: Path) -> None:
    path = tmp_path / "doctor.json"
    payload = DoctorConfig().to_dict()
    payload["schema_version"] = "romeo.hardware_calibration.v999"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(DoctorConfigVersionError, match="unsupported config schema"):
        load_config(path)


def test_invalid_calibration_is_rejected_on_load(tmp_path: Path) -> None:
    path = tmp_path / "doctor.json"
    payload = DoctorConfig(unit_calibration=CalibrationValues()).to_dict()
    assert isinstance(payload["unit_calibration"], dict)
    payload["unit_calibration"]["speed_limit"] = -1
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(DoctorConfigInvalidError, match="speed_limit"):
        load_config(path)


def test_unknown_fields_are_rejected_to_avoid_persisting_secrets(tmp_path: Path) -> None:
    path = tmp_path / "doctor.json"
    payload = DoctorConfig().to_dict()
    payload["token"] = "not-allowed"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(DoctorConfigInvalidError, match="unknown field.*token"):
        load_config(path)


def test_atomic_save_preserves_existing_file_when_replace_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "doctor.json"
    save_config(path, DoctorConfig())
    original = path.read_bytes()

    def fail_replace(source: Path, destination: Path) -> None:
        raise OSError("simulated replace failure")

    monkeypatch.setattr("romeo.doctor.config.os.replace", fail_replace)

    with pytest.raises(DoctorConfigError, match="cannot save"):
        save_config(
            path,
            DoctorConfig(
                unit_calibration=CalibrationValues(speed_limit=0.2),
                commissioning=CommissioningRecord(status="commissioned"),
            ),
        )

    assert path.read_bytes() == original
    assert not list(tmp_path.glob("*.tmp"))
