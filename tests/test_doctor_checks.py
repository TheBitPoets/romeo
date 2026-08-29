from __future__ import annotations

import json
from pathlib import Path

import pytest

from romeo.backends.mock import MockBackend
from romeo.doctor import checks as doctor_checks
from romeo.doctor.checks import run_preflight
from romeo.doctor.config import save_config
from romeo.doctor.identity import fingerprint_unit_identifier
from romeo.doctor.models import CalibrationValues, CommissioningRecord, DoctorConfig
from romeo.doctor.render import render_json, render_text
from romeo.safety import SafetyBackend

UNIT_A = "raw-raspberry-serial-unit-a"
UNIT_B = "raw-raspberry-serial-unit-b"


class FakeCamera:
    def __init__(self, *, available: bool = True, close_error: bool = False) -> None:
        self._available = available
        self.close_error = close_error

    @property
    def available(self) -> bool:
        return self._available

    def close(self) -> None:
        if self.close_error:
            raise RuntimeError("close failed")


class BrokenCloseBackend(SafetyBackend):
    def close(self) -> None:
        super().close()
        raise RuntimeError("stop confirmation failed")


class FakeRouteSocket:
    def __enter__(self) -> FakeRouteSocket:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def connect(self, _target: object) -> None:
        return None

    def getsockname(self) -> tuple[str, int]:
        return ("192.168.1.61", 49152)


def commissioned_config(version: str = "0.1.0") -> DoctorConfig:
    return DoctorConfig(
        unit_calibration=CalibrationValues(speed_limit=0.2, watchdog_timeout=0.5),
        commissioning=CommissioningRecord(
            status="commissioned",
            timestamp="2026-08-21T12:00:00Z",
            package_version=version,
            hardware_fingerprint=fingerprint_unit_identifier(UNIT_A),
            watchdog_samples_ms=(505.0, 510.0, 508.0),
        ),
    )


def run_ready(path: Path, **overrides: object):  # type: ignore[no-untyped-def]
    arguments = {
        "environ": {"ROMEO_BACKEND": "crickit"},
        "package_version_fn": lambda: "0.1.0",
        "backend_factory": lambda _name: SafetyBackend(
            MockBackend(),
            max_speed=0.2,
            command_timeout=0.5,
            background_watchdog=False,
        ),
        "camera_factory": FakeCamera,
        "network_probe": lambda: ["192.0.2.10"],
        "i2c_exists": lambda _path: True,
        "unit_identifier_provider": lambda: UNIT_A,
    }
    arguments.update(overrides)
    return run_preflight(path, **arguments)  # type: ignore[arg-type]


def test_network_probe_uses_route_when_hostname_resolves_only_to_loopback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        doctor_checks.socket,
        "getaddrinfo",
        lambda *_args: [
            (
                doctor_checks.socket.AF_INET,
                doctor_checks.socket.SOCK_STREAM,
                6,
                "",
                ("127.0.1.1", 0),
            )
        ],
    )

    def socket_factory(family: int, _kind: int) -> FakeRouteSocket:
        if family == doctor_checks.socket.AF_INET:
            return FakeRouteSocket()
        raise OSError("IPv6 route unavailable")

    monkeypatch.setattr(doctor_checks.socket, "socket", socket_factory)

    assert doctor_checks._network_addresses() == ["192.168.1.61"]


def test_everything_ok_is_ready_and_server_is_skipped(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config())

    report = run_ready(path)

    assert report.ready
    assert report.status == "ready"
    assert {check.id: check.status for check in report.checks}["server"] == "skipped"
    assert report.to_dict()["schema_version"] == "romeo.hardware_diagnostic.v1"
    identity = next(check for check in report.checks if check.id == "unit_identity")
    assert identity.status == "passed"
    assert identity.measured == {"fingerprint": fingerprint_unit_identifier(UNIT_A)}


def test_copied_calibration_is_rejected_on_another_unit(tmp_path: Path) -> None:
    path = tmp_path / "copied-from-unit-a.json"
    save_config(path, commissioned_config())

    report = run_ready(path, unit_identifier_provider=lambda: UNIT_B)

    identity = next(check for check in report.checks if check.id == "unit_identity")
    assert identity.status == "failed"
    assert not report.ready
    assert identity.measured == {
        "recorded_fingerprint": fingerprint_unit_identifier(UNIT_A),
        "current_fingerprint": fingerprint_unit_identifier(UNIT_B),
    }


def test_missing_unit_fingerprint_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "legacy.json"
    config = commissioned_config()
    save_config(
        path,
        DoctorConfig(
            unit_calibration=config.unit_calibration,
            commissioning=CommissioningRecord(
                status="commissioned",
                timestamp="2026-08-21T12:00:00Z",
                package_version="0.1.0",
                watchdog_samples_ms=(505.0, 510.0, 508.0),
            ),
        ),
    )

    report = run_ready(path)

    assert not report.ready
    assert next(check for check in report.checks if check.id == "unit_identity").status == (
        "failed"
    )


@pytest.mark.parametrize(
    "provider",
    [
        lambda: "",
        lambda: (_ for _ in ()).throw(OSError("raw-raspberry-serial-unit-a")),
    ],
    ids=["identifier-unavailable", "provider-error"],
)
def test_unverifiable_unit_identity_fails_without_raw_output(
    tmp_path: Path, provider
) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config())

    report = run_ready(path, unit_identifier_provider=provider)
    json_output = render_json(report)
    text_output = render_text(report)

    assert not report.ready
    assert next(check for check in report.checks if check.id == "unit_identity").status == (
        "failed"
    )
    assert UNIT_A not in json_output
    assert UNIT_A not in text_output


def test_matching_raw_identifier_is_never_exposed(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config())

    report = run_ready(path)

    assert report.ready
    assert UNIT_A not in render_json(report)
    assert UNIT_A not in render_text(report)


@pytest.mark.parametrize(
    ("overrides", "failed_id"),
    [
        ({"backend_factory": lambda _name: (_ for _ in ()).throw(RuntimeError())}, "crickit"),
        ({"i2c_exists": lambda _path: False}, "i2c"),
        ({"camera_factory": lambda: FakeCamera(available=False)}, "camera"),
        ({"network_probe": lambda: []}, "network"),
    ],
)
def test_blocking_hardware_failure_is_not_ready(
    tmp_path: Path, overrides: dict[str, object], failed_id: str
) -> None:
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config())

    report = run_ready(path, **overrides)

    assert not report.ready
    assert {check.id: check.status for check in report.checks}[failed_id] == "failed"


def test_missing_calibration_skips_watchdog_and_speed_limit(tmp_path: Path) -> None:
    report = run_ready(tmp_path / "missing.json")
    statuses = {check.id: check.status for check in report.checks}

    assert not report.ready
    assert statuses["calibration"] == "failed"
    assert statuses["watchdog"] == "skipped"
    assert statuses["speed_limit"] == "skipped"


def test_corrupt_or_missing_watchdog_config_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    payload = commissioned_config().to_dict()
    assert isinstance(payload["unit_calibration"], dict)
    del payload["unit_calibration"]["watchdog_timeout"]
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = run_ready(path)
    statuses = {check.id: check.status for check in report.checks}

    assert statuses["calibration"] == "failed"
    assert statuses["watchdog"] == "skipped"
    assert not report.ready


def test_package_version_mismatch_invalidates_commissioning(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config("0.0.9"))

    report = run_ready(path)

    calibration = next(check for check in report.checks if check.id == "calibration")
    assert calibration.status == "failed"
    assert calibration.measured == {
        "commissioned_package": "0.0.9",
        "installed_package": "0.1.0",
    }


def test_warning_does_not_block_ready_state(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config())

    report = run_ready(path, camera_factory=lambda: FakeCamera(close_error=True))

    assert report.ready
    assert any(check.status == "warning" for check in report.checks)


@pytest.mark.parametrize(
    ("max_speed", "timeout", "failed_id"),
    [(0.3, 0.5, "speed_limit"), (0.2, 0.8, "watchdog")],
)
def test_less_conservative_effective_safety_override_blocks_ready(
    tmp_path: Path, max_speed: float, timeout: float, failed_id: str
) -> None:
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config())

    report = run_ready(
        path,
        backend_factory=lambda _name: SafetyBackend(
            MockBackend(),
            max_speed=max_speed,
            command_timeout=timeout,
            background_watchdog=False,
        ),
    )

    assert not report.ready
    assert {check.id: check.status for check in report.checks}[failed_id] == "failed"


def test_commissioning_without_watchdog_measurements_is_not_ready(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    config = commissioned_config()
    save_config(
        path,
        DoctorConfig(
            unit_calibration=config.unit_calibration,
            commissioning=CommissioningRecord(
                status="commissioned",
                timestamp="2026-08-21T12:00:00Z",
                package_version="0.1.0",
            ),
        ),
    )

    report = run_ready(path)

    assert not report.ready
    watchdog = next(check for check in report.checks if check.id == "watchdog")
    assert watchdog.status == "failed"


def test_stale_slow_watchdog_measurements_are_not_ready(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    config = commissioned_config()
    save_config(
        path,
        DoctorConfig(
            unit_calibration=config.unit_calibration,
            commissioning=CommissioningRecord(
                status="commissioned",
                timestamp="2026-08-21T12:00:00Z",
                package_version="0.1.0",
                watchdog_samples_ms=(900.0, 950.0, 1000.0),
            ),
        ),
    )

    report = run_ready(path)

    watchdog = next(check for check in report.checks if check.id == "watchdog")
    assert watchdog.status == "failed"
    assert not report.ready


def test_backend_close_failure_blocks_ready_state(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config())

    report = run_ready(
        path,
        backend_factory=lambda _name: BrokenCloseBackend(
            MockBackend(), background_watchdog=False
        ),
    )

    assert not report.ready
    assert {check.id: check.status for check in report.checks}["crickit_close"] == "failed"


def test_mock_backend_is_rejected_without_touching_hardware(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    save_config(path, commissioned_config())

    report = run_ready(path, environ={"ROMEO_BACKEND": "mock"})
    statuses = {check.id: check.status for check in report.checks}

    assert statuses["backend"] == "failed"
    assert statuses["i2c"] == "skipped"
    assert statuses["crickit"] == "skipped"
