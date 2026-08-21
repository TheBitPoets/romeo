import json
import math
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

from romeo.doctor.models import (
    CONFIG_SCHEMA_VERSION,
    REPORT_SCHEMA_VERSION,
    CalibrationValues,
    CheckResult,
    CommissioningRecord,
    DiagnosticReport,
    DoctorConfig,
    ModelValidationError,
)


def test_config_round_trip_keeps_defaults_calibration_and_commissioning_separate() -> None:
    calibration = CalibrationValues(left_inverted=True, left_trim=0.1, speed_limit=0.4)
    config = DoctorConfig(
        unit_calibration=calibration,
        commissioning=CommissioningRecord(
            status="commissioned",
            timestamp="2026-08-21T10:30:00+02:00",
            package_version="0.1.0",
            hardware_fingerprint="rpi5-crickit-a",
        ),
    )

    restored = DoctorConfig.from_dict(config.to_dict())

    assert restored == config
    assert restored.schema_version == CONFIG_SCHEMA_VERSION
    assert restored.model_defaults.left_inverted is False
    assert restored.unit_calibration == calibration


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"speed_limit": float("nan")}, "finite"),
        ({"speed_limit": float("inf")}, "finite"),
        ({"speed_limit": 0.0}, "between"),
        ({"left_trim": 1.1}, "between"),
        ({"watchdog_timeout": 0.0}, "between"),
        ({"pan_min": 100.0, "pan_max": 90.0}, "pan_min"),
        ({"tilt_min": 100.0, "tilt_max": 90.0}, "tilt_min"),
    ],
)
def test_calibration_rejects_non_finite_and_out_of_range_values(
    changes: dict[str, float], message: str
) -> None:
    with pytest.raises(ModelValidationError, match=message):
        CalibrationValues(**changes)


def test_strict_parser_rejects_unknown_and_missing_fields() -> None:
    data = DoctorConfig().to_dict()
    data["secret"] = "must-not-be-accepted"
    with pytest.raises(ModelValidationError, match="unknown field.*secret"):
        DoctorConfig.from_dict(data)

    calibration = CalibrationValues().to_dict()
    del calibration["speed_limit"]
    with pytest.raises(ModelValidationError, match="missing field.*speed_limit"):
        CalibrationValues.from_dict(calibration)


def test_strict_parser_does_not_treat_booleans_as_numbers() -> None:
    calibration = CalibrationValues().to_dict()
    calibration["speed_limit"] = True

    with pytest.raises(ModelValidationError, match="must be a number"):
        CalibrationValues.from_dict(calibration)


def test_commissioning_timestamp_requires_timezone() -> None:
    with pytest.raises(ModelValidationError, match="timezone"):
        CommissioningRecord(status="commissioned", timestamp="2026-08-21T10:30:00")


def test_diagnostic_report_has_versioned_json_shape() -> None:
    report = DiagnosticReport(
        status="ready",
        ready=True,
        checks=(CheckResult("python", "passed", "Python disponibile", {"major": 3}),),
        calibration={"speed_limit": 0.4},
        hardware={"backend": "crickit"},
    )

    payload = report.to_dict()

    assert payload["schema_version"] == REPORT_SCHEMA_VERSION
    assert payload["checks"][0]["status"] == "passed"
    assert payload["ready"] is True


@pytest.mark.parametrize("value", [math.nan, math.inf, object()])
def test_check_measured_must_be_safe_json(value: object) -> None:
    with pytest.raises(ModelValidationError, match="measured"):
        CheckResult("camera", "failed", "Camera non disponibile", value)


def test_report_ready_flag_must_match_status() -> None:
    with pytest.raises(ModelValidationError, match="ready must be true"):
        DiagnosticReport(status="ready", ready=False, checks=())


def test_published_diagnostic_schema_enforces_ready_invariant() -> None:
    schema = json.loads(
        Path("docs/hardware/schemas/romeo.hardware_diagnostic.v1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    payload = DiagnosticReport(status="ready", ready=True, checks=()).to_dict()
    validator = Draft202012Validator(schema)

    validator.validate(payload)
    payload["status"] = "preflight_failed"
    with pytest.raises(ValidationError):
        validator.validate(payload)


def test_published_calibration_schema_requires_timezone_date_time() -> None:
    schema = json.loads(
        Path("docs/hardware/schemas/romeo.hardware_calibration.v1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    payload = DoctorConfig(
        commissioning=CommissioningRecord(
            status="commissioned",
            timestamp="2026-08-21T10:30:00+02:00",
            package_version="0.2.0",
        )
    ).to_dict()
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    validator.validate(payload)
    payload["commissioning"]["timestamp"] = "2026-08-21T10:30:00"
    with pytest.raises(ValidationError):
        validator.validate(payload)
