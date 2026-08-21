"""Versioned data models shared by the Romeo hardware doctor."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

CONFIG_SCHEMA_VERSION = "romeo.hardware_calibration.v1"
REPORT_SCHEMA_VERSION = "romeo.hardware_diagnostic.v1"

CheckStatus = Literal["passed", "failed", "skipped", "warning"]
DoctorStatus = Literal["not_commissioned", "commissioned", "preflight_failed", "ready"]

_CHECK_STATUSES = {"passed", "failed", "skipped", "warning"}
_DOCTOR_STATUSES = {"not_commissioned", "commissioned", "preflight_failed", "ready"}


class ModelValidationError(ValueError):
    """Raised when doctor data does not match its declared schema."""


def _object(value: object, path: str) -> dict[str, Any]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ModelValidationError(f"{path} must be a JSON object")
    return value


def _only_keys(data: dict[str, Any], allowed: set[str], path: str) -> None:
    unknown = set(data) - allowed
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ModelValidationError(f"{path} contains unknown field(s): {names}")


def _required(data: dict[str, Any], name: str, path: str) -> Any:
    if name not in data:
        raise ModelValidationError(f"{path}.{name} is required")
    return data[name]


def _number(value: object, path: str, *, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ModelValidationError(f"{path} must be a number")
    result = float(value)
    if not math.isfinite(result) or not minimum <= result <= maximum:
        raise ModelValidationError(
            f"{path} must be finite and between {minimum:g} and {maximum:g}"
        )
    return result


def _boolean(value: object, path: str) -> bool:
    if not isinstance(value, bool):
        raise ModelValidationError(f"{path} must be a boolean")
    return value


def _optional_string(value: object, path: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ModelValidationError(f"{path} must be null or a non-empty string")
    return value


def _json_value(value: object, path: str) -> Any:
    """Validate JSON-compatible diagnostic data, rejecting NaN and infinities."""

    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(float(value)):
            raise ModelValidationError(f"{path} must not contain NaN or infinity")
        return value
    if isinstance(value, list):
        return [_json_value(item, f"{path}[{index}]") for index, item in enumerate(value)]
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        return {key: _json_value(item, f"{path}.{key}") for key, item in value.items()}
    raise ModelValidationError(f"{path} must be JSON-serializable")


@dataclass(frozen=True, slots=True)
class CalibrationValues:
    """Motor, servo, and safety values for a Romeo model or physical unit."""

    left_inverted: bool = False
    right_inverted: bool = False
    left_trim: float = 0.0
    right_trim: float = 0.0
    speed_limit: float = 0.7
    pan_min: float = 0.0
    pan_max: float = 180.0
    tilt_min: float = 0.0
    tilt_max: float = 180.0
    watchdog_timeout: float = 1.0

    def __post_init__(self) -> None:
        for name in ("left_inverted", "right_inverted"):
            if not isinstance(getattr(self, name), bool):
                raise ModelValidationError(f"{name} must be a boolean")
        for name in ("left_trim", "right_trim"):
            _number(getattr(self, name), name, minimum=-1.0, maximum=1.0)
        _number(self.speed_limit, "speed_limit", minimum=0.01, maximum=1.0)
        for name in ("pan_min", "pan_max", "tilt_min", "tilt_max"):
            _number(getattr(self, name), name, minimum=0.0, maximum=180.0)
        _number(self.watchdog_timeout, "watchdog_timeout", minimum=0.05, maximum=10.0)
        if self.pan_min >= self.pan_max:
            raise ModelValidationError("pan_min must be less than pan_max")
        if self.tilt_min >= self.tilt_max:
            raise ModelValidationError("tilt_min must be less than tilt_max")

    def to_dict(self) -> dict[str, object]:
        return {name: getattr(self, name) for name in _CALIBRATION_FIELDS}

    @classmethod
    def from_dict(cls, value: object, path: str = "calibration") -> CalibrationValues:
        data = _object(value, path)
        _only_keys(data, set(_CALIBRATION_FIELDS), path)
        missing = set(_CALIBRATION_FIELDS) - set(data)
        if missing:
            raise ModelValidationError(f"{path} is missing field(s): {', '.join(sorted(missing))}")
        return cls(
            left_inverted=_boolean(data["left_inverted"], f"{path}.left_inverted"),
            right_inverted=_boolean(data["right_inverted"], f"{path}.right_inverted"),
            left_trim=_number(data["left_trim"], f"{path}.left_trim", minimum=-1, maximum=1),
            right_trim=_number(data["right_trim"], f"{path}.right_trim", minimum=-1, maximum=1),
            speed_limit=_number(
                data["speed_limit"], f"{path}.speed_limit", minimum=0.01, maximum=1
            ),
            pan_min=_number(data["pan_min"], f"{path}.pan_min", minimum=0, maximum=180),
            pan_max=_number(data["pan_max"], f"{path}.pan_max", minimum=0, maximum=180),
            tilt_min=_number(data["tilt_min"], f"{path}.tilt_min", minimum=0, maximum=180),
            tilt_max=_number(data["tilt_max"], f"{path}.tilt_max", minimum=0, maximum=180),
            watchdog_timeout=_number(
                data["watchdog_timeout"],
                f"{path}.watchdog_timeout",
                minimum=0.05,
                maximum=10,
            ),
        )


_CALIBRATION_FIELDS = (
    "left_inverted",
    "right_inverted",
    "left_trim",
    "right_trim",
    "speed_limit",
    "pan_min",
    "pan_max",
    "tilt_min",
    "tilt_max",
    "watchdog_timeout",
)


@dataclass(frozen=True, slots=True)
class CommissioningRecord:
    """Non-sensitive evidence describing the last commissioning state."""

    status: DoctorStatus = "not_commissioned"
    timestamp: str | None = None
    package_version: str | None = None
    hardware_fingerprint: str | None = None
    watchdog_samples_ms: tuple[float, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in _DOCTOR_STATUSES:
            raise ModelValidationError(f"unknown commissioning status: {self.status}")
        for name in ("timestamp", "package_version", "hardware_fingerprint"):
            _optional_string(getattr(self, name), name)
        if not isinstance(self.watchdog_samples_ms, tuple):
            raise ModelValidationError("watchdog_samples_ms must be a tuple")
        if len(self.watchdog_samples_ms) > 20:
            raise ModelValidationError("watchdog_samples_ms must contain at most 20 samples")
        for index, sample in enumerate(self.watchdog_samples_ms):
            _number(sample, f"watchdog_samples_ms[{index}]", minimum=0.001, maximum=10_000)
        if self.timestamp is not None:
            try:
                parsed = datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
            except ValueError as error:
                raise ModelValidationError("timestamp must be ISO 8601") from error
            if parsed.tzinfo is None:
                raise ModelValidationError("timestamp must include a timezone")

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "timestamp": self.timestamp,
            "package_version": self.package_version,
            "hardware_fingerprint": self.hardware_fingerprint,
            "watchdog_samples_ms": list(self.watchdog_samples_ms),
        }

    @classmethod
    def from_dict(cls, value: object) -> CommissioningRecord:
        path = "commissioning"
        data = _object(value, path)
        fields = {
            "status",
            "timestamp",
            "package_version",
            "hardware_fingerprint",
            "watchdog_samples_ms",
        }
        _only_keys(data, fields, path)
        status = _required(data, "status", path)
        if not isinstance(status, str) or status not in _DOCTOR_STATUSES:
            raise ModelValidationError(f"{path}.status is invalid")
        return cls(
            status=status,  # type: ignore[arg-type]
            timestamp=_optional_string(data.get("timestamp"), f"{path}.timestamp"),
            package_version=_optional_string(
                data.get("package_version"), f"{path}.package_version"
            ),
            hardware_fingerprint=_optional_string(
                data.get("hardware_fingerprint"), f"{path}.hardware_fingerprint"
            ),
            watchdog_samples_ms=_samples(
                _required(data, "watchdog_samples_ms", path),
                f"{path}.watchdog_samples_ms",
            ),
        )


def _samples(value: object, path: str) -> tuple[float, ...]:
    if not isinstance(value, list):
        raise ModelValidationError(f"{path} must be a JSON array")
    return tuple(
        _number(sample, f"{path}[{index}]", minimum=0.001, maximum=10_000)
        for index, sample in enumerate(value)
    )


@dataclass(frozen=True, slots=True)
class DoctorConfig:
    """Persistent doctor configuration with model and unit values kept separate."""

    model_defaults: CalibrationValues = field(default_factory=CalibrationValues)
    unit_calibration: CalibrationValues | None = None
    commissioning: CommissioningRecord = field(default_factory=CommissioningRecord)
    schema_version: str = CONFIG_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != CONFIG_SCHEMA_VERSION:
            raise ModelValidationError(f"unsupported config schema: {self.schema_version}")
        if not isinstance(self.model_defaults, CalibrationValues):
            raise ModelValidationError("model_defaults must be CalibrationValues")
        if self.unit_calibration is not None and not isinstance(
            self.unit_calibration, CalibrationValues
        ):
            raise ModelValidationError("unit_calibration must be CalibrationValues or null")
        if not isinstance(self.commissioning, CommissioningRecord):
            raise ModelValidationError("commissioning must be CommissioningRecord")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "model_defaults": self.model_defaults.to_dict(),
            "unit_calibration": (
                self.unit_calibration.to_dict() if self.unit_calibration is not None else None
            ),
            "commissioning": self.commissioning.to_dict(),
        }

    @classmethod
    def from_dict(cls, value: object) -> DoctorConfig:
        data = _object(value, "config")
        fields = {"schema_version", "model_defaults", "unit_calibration", "commissioning"}
        _only_keys(data, fields, "config")
        version = _required(data, "schema_version", "config")
        if version != CONFIG_SCHEMA_VERSION:
            raise ModelValidationError(f"unsupported config schema: {version!r}")
        unit_data = _required(data, "unit_calibration", "config")
        return cls(
            schema_version=version,
            model_defaults=CalibrationValues.from_dict(
                _required(data, "model_defaults", "config"), "model_defaults"
            ),
            unit_calibration=(
                None
                if unit_data is None
                else CalibrationValues.from_dict(unit_data, "unit_calibration")
            ),
            commissioning=CommissioningRecord.from_dict(
                _required(data, "commissioning", "config")
            ),
        )


@dataclass(frozen=True, slots=True)
class CheckResult:
    id: str
    status: CheckStatus
    detail: str
    measured: Any = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ModelValidationError("check id must be a non-empty string")
        if self.status not in _CHECK_STATUSES:
            raise ModelValidationError(f"unknown check status: {self.status}")
        if not isinstance(self.detail, str) or not self.detail.strip():
            raise ModelValidationError("check detail must be a non-empty string")
        _json_value(self.measured, "measured")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "detail": self.detail,
            "measured": _json_value(self.measured, "measured"),
        }


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    status: DoctorStatus
    ready: bool
    checks: tuple[CheckResult, ...]
    calibration: dict[str, Any] = field(default_factory=dict)
    hardware: dict[str, Any] = field(default_factory=dict)
    schema_version: str = REPORT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != REPORT_SCHEMA_VERSION:
            raise ModelValidationError(f"unsupported report schema: {self.schema_version}")
        if self.status not in _DOCTOR_STATUSES:
            raise ModelValidationError(f"unknown doctor status: {self.status}")
        if not isinstance(self.ready, bool):
            raise ModelValidationError("ready must be a boolean")
        if self.ready != (self.status == "ready"):
            raise ModelValidationError("ready must be true exactly when status is 'ready'")
        if not isinstance(self.checks, tuple) or any(
            not isinstance(check, CheckResult) for check in self.checks
        ):
            raise ModelValidationError("checks must be a tuple of CheckResult values")
        _json_value(self.calibration, "calibration")
        _json_value(self.hardware, "hardware")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "ready": self.ready,
            "checks": [check.to_dict() for check in self.checks],
            "calibration": _json_value(self.calibration, "calibration"),
            "hardware": _json_value(self.hardware, "hardware"),
        }
