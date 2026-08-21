"""Reusable models and configuration for Romeo hardware diagnostics."""

from romeo.doctor.config import (
    DoctorConfigError,
    DoctorConfigInvalidError,
    DoctorConfigVersionError,
    default_config_path,
    load_config,
    save_config,
)
from romeo.doctor.identity import (
    UnitIdentityError,
    fingerprint_unit_identifier,
    is_unit_fingerprint,
    read_raspberry_unit_identifier,
)
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

__all__ = [
    "CONFIG_SCHEMA_VERSION",
    "REPORT_SCHEMA_VERSION",
    "CalibrationValues",
    "CheckResult",
    "CommissioningRecord",
    "DiagnosticReport",
    "DoctorConfig",
    "DoctorConfigError",
    "DoctorConfigInvalidError",
    "DoctorConfigVersionError",
    "default_config_path",
    "ModelValidationError",
    "UnitIdentityError",
    "fingerprint_unit_identifier",
    "is_unit_fingerprint",
    "load_config",
    "read_raspberry_unit_identifier",
    "save_config",
]
