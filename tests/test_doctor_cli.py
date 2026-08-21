from __future__ import annotations

from pathlib import Path

import pytest

from romeo.backends.mock import MockBackend
from romeo.camera.mock import MockCameraService
from romeo.doctor import cli
from romeo.doctor.config import load_config
from romeo.doctor.identity import UnitIdentityError, fingerprint_unit_identifier
from romeo.doctor.models import CheckResult, DiagnosticReport
from romeo.safety import SafetyBackend


def test_cli_exit_code_zero_only_when_ready(monkeypatch, capsys) -> None:  # type: ignore[no-untyped-def]
    ready = DiagnosticReport(
        status="ready", ready=True, checks=(CheckResult("python", "passed", "OK"),)
    )
    monkeypatch.setattr(cli, "run_preflight", lambda _path: ready)

    assert cli.main(["--json"]) == cli.EXIT_READY
    assert '"ready": true' in capsys.readouterr().out

    failed = DiagnosticReport(
        status="preflight_failed",
        ready=False,
        checks=(CheckResult("camera", "failed", "assente"),),
    )
    monkeypatch.setattr(cli, "run_preflight", lambda _path: failed)

    assert cli.main([]) == cli.EXIT_NOT_READY
    assert "non è pronto" in capsys.readouterr().out


def test_commissioning_cancel_does_not_save(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    raw_backend = MockBackend()
    backend = SafetyBackend(raw_backend, command_timeout=0.05)

    result = cli.run_commissioning(
        path,
        backend,
        input_fn=lambda _prompt: "q",
        output_fn=lambda _message: None,
        camera_factory=MockCameraService,
        package_version="0.1.0",
        unit_identifier_provider=lambda: "unit-a-raw-serial",
    )

    assert result == cli.EXIT_CANCELLED
    assert not path.exists()
    assert raw_backend.left_speed == raw_backend.right_speed == 0.0
    backend.close()


def test_commissioning_records_polarity_trim_limits_and_camera(tmp_path: Path) -> None:
    path = tmp_path / "hardware.json"
    raw_backend = MockBackend()
    backend = SafetyBackend(raw_backend, command_timeout=0.05)
    answers = iter(
        [
            "SICURO",
            "",
            "n",
            "",
            "s",
            "0.1",
            "-0.1",
            "0.2",
            "50",
            "130",
            "55",
            "125",
            "0.5",
            "",
            "",
            "s",
            "",
            "s",
            "",
            "s",
            "",
            "s",
            "",
            "s",
            "",
            "s",
            "",
            "SALVA",
        ]
    )

    result = cli.run_commissioning(
        path,
        backend,
        input_fn=lambda _prompt: next(answers),
        output_fn=lambda _message: None,
        camera_factory=MockCameraService,
        package_version="0.1.0",
        unit_identifier_provider=lambda: "unit-a-raw-serial",
    )

    assert result == cli.EXIT_READY
    saved = load_config(path)
    assert saved.unit_calibration is not None
    assert saved.unit_calibration.left_inverted
    assert not saved.unit_calibration.right_inverted
    assert saved.unit_calibration.left_trim == 0.1
    assert saved.unit_calibration.right_trim == -0.1
    assert saved.unit_calibration.pan_min == 50.0
    assert saved.unit_calibration.tilt_max == 125.0
    assert saved.commissioning.status == "commissioned"
    assert saved.commissioning.hardware_fingerprint == fingerprint_unit_identifier(
        "unit-a-raw-serial"
    )
    assert len(saved.commissioning.watchdog_samples_ms) == 3
    assert raw_backend.left_speed == raw_backend.right_speed == 0.0
    backend.close()


def test_commissioning_without_reliable_identity_does_not_move_or_save(
    tmp_path: Path,
) -> None:
    path = tmp_path / "hardware.json"
    raw_backend = MockBackend()
    backend = SafetyBackend(raw_backend, command_timeout=0.05)

    with pytest.raises(UnitIdentityError):
        cli.run_commissioning(
            path,
            backend,
            input_fn=lambda _prompt: "SICURO",
            output_fn=lambda _message: None,
            camera_factory=MockCameraService,
            unit_identifier_provider=lambda: "",
        )

    assert not path.exists()
    assert raw_backend.left_speed == raw_backend.right_speed == 0.0
    assert all(command.name == "stop" for command in raw_backend.history)
    backend.close()


def test_cli_passes_explicit_config_to_hardware_factory(
    tmp_path: Path, monkeypatch
) -> None:  # type: ignore[no-untyped-def]
    from romeo.backends import factory

    path = tmp_path / "selected.json"
    captured: list[Path | None] = []
    backend = SafetyBackend(MockBackend(), command_timeout=0.05)

    def create(_name: str, *, config_path: Path | None = None) -> SafetyBackend:
        captured.append(config_path)
        return backend

    monkeypatch.setattr(factory, "create_backend", create)
    monkeypatch.setattr(cli, "run_commissioning", lambda *_args, **_kwargs: cli.EXIT_CANCELLED)

    assert cli.main(["--commission", "--config", str(path)]) == cli.EXIT_CANCELLED
    assert captured == [path]
