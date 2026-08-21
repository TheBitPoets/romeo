"""Backend selection without leaking infrastructure into student programs."""

import os
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

from romeo.backends.base import Backend
from romeo.backends.mock import MockBackend
from romeo.safety import SafetyBackend

_BACKEND_OVERRIDE: ContextVar[Backend | None] = ContextVar("romeo_backend_override", default=None)


def create_backend(
    name: str | None = None,
    *,
    safety: bool = True,
    config_path: str | Path | None = None,
) -> Backend:
    """Create a backend selected explicitly or through ``ROMEO_BACKEND``.

    ``mock`` is the safe default on development machines. ``sim`` uses the scenario
    named by ``ROMEO_SCENARIO`` or a small empty arena when the variable is unset.
    """

    override = _BACKEND_OVERRIDE.get()
    if override is not None:
        return override
    selected_name = name if name is not None else os.environ.get("ROMEO_BACKEND", "mock")
    backend_name = selected_name.strip().lower()
    configured_max_speed: float | None = None
    calibrated_timeout: float | None = None
    if backend_name == "mock":
        backend: Backend = MockBackend()
    elif backend_name == "crickit":
        from romeo.backends.crickit import CrickitBackend, CrickitConfig
        from romeo.doctor.config import default_config_path, load_config

        doctor_config = load_config(
            default_config_path() if config_path is None else Path(config_path)
        )
        calibration = doctor_config.unit_calibration or doctor_config.model_defaults
        configured_max_speed = float(
            os.environ.get("ROMEO_MAX_SPEED", calibration.speed_limit)
        )
        backend = CrickitBackend(
            config=CrickitConfig(
                left_motor_inverted=calibration.left_inverted,
                right_motor_inverted=calibration.right_inverted,
                left_trim=calibration.left_trim,
                right_trim=calibration.right_trim,
                max_speed=configured_max_speed,
                pan_min=calibration.pan_min,
                pan_max=calibration.pan_max,
                tilt_min=calibration.tilt_min,
                tilt_max=calibration.tilt_max,
            )
        )
        calibrated_timeout = calibration.watchdog_timeout
    elif backend_name == "sim":
        from romeo.simulation.engine import SimulationEngine
        from romeo.simulation.scenario import SCENARIO_SCHEMA, Scenario

        scenario_path = os.environ.get("ROMEO_SCENARIO")
        scenario = (
            Scenario.from_json(Path(scenario_path))
            if scenario_path
            else Scenario.from_mapping({"schema_version": SCENARIO_SCHEMA, "id": "default-arena"})
        )
        backend = SimulationEngine(scenario)
    else:
        raise ValueError(f"unknown Romeo backend: {backend_name!r}")
    if not safety or backend_name == "sim":
        return backend
    max_speed = (
        configured_max_speed
        if configured_max_speed is not None
        else float(os.environ.get("ROMEO_MAX_SPEED", 0.7))
    )
    command_timeout = float(
        os.environ.get("ROMEO_COMMAND_TIMEOUT", calibrated_timeout or 1.0)
    )
    return SafetyBackend(backend, max_speed=max_speed, command_timeout=command_timeout)


@contextmanager
def backend_override(backend: Backend) -> Iterator[None]:
    """Bind one host-provided backend while a submission or embedded app runs."""

    token = _BACKEND_OVERRIDE.set(backend)
    try:
        yield
    finally:
        _BACKEND_OVERRIDE.reset(token)
