import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from romeo.backends.crickit import CrickitBackend, CrickitConfig
from romeo.backends.factory import create_backend
from romeo.doctor.config import save_config
from romeo.doctor.models import CalibrationValues, DoctorConfig
from romeo.safety import SafetyBackend


class Pixel:
    def fill(self, _color: int) -> None:
        return


def board() -> SimpleNamespace:
    return SimpleNamespace(
        dc_motor_1=SimpleNamespace(throttle=None),
        dc_motor_2=SimpleNamespace(throttle=None),
        servo_1=SimpleNamespace(angle=None),
        servo_4=SimpleNamespace(angle=None),
        onboard_pixel=Pixel(),
    )


def test_crickit_factory_consumes_unit_calibration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "hardware.json"
    save_config(
        path,
        DoctorConfig(
            unit_calibration=CalibrationValues(
                left_inverted=True,
                left_trim=-0.25,
                right_trim=0.5,
                speed_limit=0.2,
                pan_min=40,
                pan_max=140,
                tilt_min=50,
                tilt_max=130,
                watchdog_timeout=0.5,
            )
        ),
    )
    hardware = board()
    monkeypatch.setitem(sys.modules, "adafruit_crickit", SimpleNamespace(crickit=hardware))
    monkeypatch.setenv("ROMEO_DOCTOR_CONFIG", str(path))
    monkeypatch.delenv("ROMEO_MAX_SPEED", raising=False)
    monkeypatch.delenv("ROMEO_COMMAND_TIMEOUT", raising=False)

    backend = create_backend("crickit")
    assert isinstance(backend, SafetyBackend)
    assert isinstance(backend.backend, CrickitBackend)
    assert backend.max_speed == 0.2
    assert backend.command_timeout == 0.5

    backend.set_motor_speeds(0.2, 0.2)
    assert hardware.dc_motor_2.throttle == pytest.approx(-0.15)
    assert hardware.dc_motor_1.throttle == pytest.approx(0.2)
    backend.set_camera_angles(0, 180)
    assert hardware.servo_1.angle == 40
    assert hardware.servo_4.angle == 130
    backend.close()


def test_explicit_safety_environment_overrides_calibration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "hardware.json"
    save_config(
        path,
        DoctorConfig(
            unit_calibration=CalibrationValues(speed_limit=0.2, watchdog_timeout=0.5)
        ),
    )
    hardware = board()
    monkeypatch.setitem(sys.modules, "adafruit_crickit", SimpleNamespace(crickit=hardware))
    monkeypatch.setenv("ROMEO_DOCTOR_CONFIG", str(path))
    monkeypatch.setenv("ROMEO_MAX_SPEED", "0.15")
    monkeypatch.setenv("ROMEO_COMMAND_TIMEOUT", "0.25")

    backend = create_backend("crickit")

    assert isinstance(backend, SafetyBackend)
    assert backend.max_speed == 0.15
    assert backend.command_timeout == 0.25
    backend.set_motor_speeds(0.15, 0.15)
    assert hardware.dc_motor_1.throttle == 0.15
    backend.close()


def test_explicit_config_path_takes_precedence_over_default_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    default_path = tmp_path / "default.json"
    explicit_path = tmp_path / "selected.json"
    save_config(
        default_path,
        DoctorConfig(unit_calibration=CalibrationValues(speed_limit=0.7)),
    )
    save_config(
        explicit_path,
        DoctorConfig(unit_calibration=CalibrationValues(speed_limit=0.2)),
    )
    hardware = board()
    monkeypatch.setitem(sys.modules, "adafruit_crickit", SimpleNamespace(crickit=hardware))
    monkeypatch.setenv("ROMEO_DOCTOR_CONFIG", str(default_path))
    monkeypatch.delenv("ROMEO_MAX_SPEED", raising=False)

    backend = create_backend("crickit", config_path=explicit_path)

    assert isinstance(backend, SafetyBackend)
    assert backend.max_speed == 0.2
    backend.close()


def test_crickit_reconfiguration_tests_candidate_servo_limits() -> None:
    hardware = board()
    backend = CrickitBackend(
        board=hardware,
        config=CrickitConfig(pan_min=60, pan_max=120, tilt_min=60, tilt_max=120),
    )

    backend.configure(CrickitConfig(pan_min=30, pan_max=150, tilt_min=40, tilt_max=140))
    backend.set_camera_angles(30, 40)

    assert hardware.servo_1.angle == 30
    assert hardware.servo_4.angle == 40
