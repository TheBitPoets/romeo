"""Safe persistent storage for Romeo Doctor calibration."""

from __future__ import annotations

import json
import os
import tempfile
from contextlib import suppress
from pathlib import Path

from romeo.doctor.models import DoctorConfig, ModelValidationError


class DoctorConfigError(RuntimeError):
    """Base class for configuration read and write failures."""


class DoctorConfigInvalidError(DoctorConfigError):
    """Raised when a configuration file is corrupt or fails validation."""


class DoctorConfigVersionError(DoctorConfigInvalidError):
    """Raised when a configuration uses an unsupported schema version."""


def default_config_path(environ: dict[str, str] | None = None) -> Path:
    """Return the per-unit calibration path without creating it.

    ``ROMEO_DOCTOR_CONFIG`` is an explicit administrative override.  Linux
    installations otherwise follow XDG, while Windows uses the roaming app
    data directory when available.
    """

    environment = os.environ if environ is None else environ
    explicit = environment.get("ROMEO_DOCTOR_CONFIG")
    if explicit:
        return Path(explicit).expanduser()
    xdg_home = environment.get("XDG_CONFIG_HOME")
    if xdg_home:
        return Path(xdg_home).expanduser() / "romeo" / "hardware.json"
    app_data = environment.get("APPDATA")
    if os.name == "nt" and app_data:
        return Path(app_data).expanduser() / "Romeo" / "hardware.json"
    return Path.home() / ".config" / "romeo" / "hardware.json"


def load_config(path: str | Path) -> DoctorConfig:
    """Load a config, returning an uncommissioned default when it is absent."""

    config_path = Path(path)
    try:
        text = config_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return DoctorConfig()
    except OSError as error:
        raise DoctorConfigError(f"cannot read Romeo Doctor config: {config_path}") from error

    try:
        raw = json.loads(text)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise DoctorConfigInvalidError(
            f"invalid JSON in Romeo Doctor config: {config_path}"
        ) from error

    try:
        return DoctorConfig.from_dict(raw)
    except ModelValidationError as error:
        if "unsupported config schema" in str(error):
            raise DoctorConfigVersionError(str(error)) from error
        raise DoctorConfigInvalidError(str(error)) from error


def save_config(path: str | Path, config: DoctorConfig) -> None:
    """Atomically replace a configuration file with validated JSON."""

    if not isinstance(config, DoctorConfig):
        raise TypeError("config must be a DoctorConfig")
    # Re-parse the serialized representation so invalid nested mutations cannot be persisted.
    DoctorConfig.from_dict(config.to_dict())
    config_path = Path(path)
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise DoctorConfigError(f"cannot create config directory: {config_path.parent}") from error

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=config_path.parent,
            prefix=f".{config_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(config.to_dict(), temporary, ensure_ascii=False, indent=2, sort_keys=True)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, config_path)
        temporary_path = None
    except (OSError, TypeError, ValueError) as error:
        raise DoctorConfigError(f"cannot save Romeo Doctor config: {config_path}") from error
    finally:
        if temporary_path is not None:
            with suppress(FileNotFoundError):
                temporary_path.unlink()
