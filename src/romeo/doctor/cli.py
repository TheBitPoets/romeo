"""Command-line preflight and supervised commissioning for physical Romeo units."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
from collections.abc import Callable, Sequence
from contextlib import suppress
from datetime import datetime, timezone
from pathlib import Path

from romeo.backends.base import Backend
from romeo.backends.crickit import CrickitBackend, CrickitConfig
from romeo.camera.base import CameraService
from romeo.doctor.checks import run_preflight
from romeo.doctor.commission import CommissionExecutor, MotorObservation
from romeo.doctor.config import (
    DoctorConfigError,
    default_config_path,
    load_config,
    save_config,
)
from romeo.doctor.models import CalibrationValues, CommissioningRecord, DoctorConfig
from romeo.doctor.render import render_json, render_text
from romeo.safety import SafetyBackend

EXIT_READY = 0
EXIT_NOT_READY = 1
EXIT_CANCELLED = 2
EXIT_ERROR = 3

Input = Callable[[str], str]
Output = Callable[[str], None]
CameraFactory = Callable[[], CameraService]


def _version() -> str:
    return importlib.metadata.version("thebitlab-romeo")


def _ask_number(input_fn: Input, label: str, default: float) -> float:
    answer = input_fn(f"{label} [{default:g}]: ").strip()
    try:
        return default if not answer else float(answer.replace(",", "."))
    except ValueError as error:
        raise ValueError(f"{label}: inserisci un numero") from error


def _camera_factory() -> CameraService:
    from romeo.camera.picamera2 import Picamera2CameraService

    return Picamera2CameraService()


def run_commissioning(
    config_path: Path,
    backend: Backend,
    *,
    input_fn: Input = input,
    output_fn: Output = print,
    camera_factory: CameraFactory = _camera_factory,
    package_version: str | None = None,
) -> int:
    """Commission one unit interactively; save only after all active checks pass."""

    config = load_config(config_path)
    base = config.unit_calibration or CalibrationValues(
        speed_limit=0.2,
        pan_min=45.0,
        pan_max=135.0,
        tilt_min=45.0,
        tilt_max=135.0,
        watchdog_timeout=0.5,
    )
    executor = CommissionExecutor(backend, input_fn=input_fn, output_fn=output_fn)
    output_fn("COMMISSIONING ROMEO — modalità attiva supervisionata")
    output_fn("Ruote sollevate, area libera e alimentazione rimovibile immediatamente.")
    if input_fn("Scrivi SICURO per iniziare, oppure q per annullare: ").strip() != "SICURO":
        backend.stop()
        output_fn("Commissioning annullato; nessuna configurazione modificata.")
        return EXIT_CANCELLED

    try:
        left = executor.test_motor("left")
        right = executor.test_motor("right")
        if left.cancelled or right.cancelled:
            return EXIT_CANCELLED
        if (
            left.observation is MotorObservation.NO_MOVEMENT
            or right.observation is MotorObservation.NO_MOVEMENT
        ):
            output_fn("Un motore non si è mosso: commissioning interrotto senza salvare.")
            return EXIT_NOT_READY

        candidate = CalibrationValues(
            left_inverted=(not base.left_inverted)
            if left.inversion_required
            else base.left_inverted,
            right_inverted=(not base.right_inverted)
            if right.inversion_required
            else base.right_inverted,
            left_trim=_ask_number(input_fn, "Trim sinistro (-1..1)", base.left_trim),
            right_trim=_ask_number(input_fn, "Trim destro (-1..1)", base.right_trim),
            speed_limit=_ask_number(input_fn, "Limite velocità (0.01..1)", base.speed_limit),
            pan_min=_ask_number(input_fn, "Pan minimo conservativo", base.pan_min),
            pan_max=_ask_number(input_fn, "Pan massimo conservativo", base.pan_max),
            tilt_min=_ask_number(input_fn, "Tilt minimo conservativo", base.tilt_min),
            tilt_max=_ask_number(input_fn, "Tilt massimo conservativo", base.tilt_max),
            watchdog_timeout=_ask_number(
                input_fn, "Watchdog in secondi", base.watchdog_timeout
            ),
        )

        if not isinstance(backend, SafetyBackend):
            raise RuntimeError("commissioning requires SafetyBackend")
        if isinstance(backend.backend, CrickitBackend):
            backend.backend.configure(
                CrickitConfig(
                    left_motor_inverted=candidate.left_inverted,
                    right_motor_inverted=candidate.right_inverted,
                    left_trim=candidate.left_trim,
                    right_trim=candidate.right_trim,
                    max_speed=candidate.speed_limit,
                    pan_min=candidate.pan_min,
                    pan_max=candidate.pan_max,
                    tilt_min=candidate.tilt_min,
                    tilt_max=candidate.tilt_max,
                )
            )
        backend.configure_max_speed(candidate.speed_limit)
        backend.configure_command_timeout(candidate.watchdog_timeout)
        watchdog = executor.measure_watchdog(repeats=3)

        center_pan = (candidate.pan_min + candidate.pan_max) / 2.0
        center_tilt = (candidate.tilt_min + candidate.tilt_max) / 2.0
        positions = (
            (center_pan, center_tilt),
            (candidate.pan_min, center_tilt),
            (candidate.pan_max, center_tilt),
            (center_pan, candidate.tilt_min),
            (center_pan, candidate.tilt_max),
            (center_pan, center_tilt),
        )
        if not all(
            executor.test_servo(
                pan,
                tilt,
                safe_pan=center_pan,
                safe_tilt=center_tilt,
            ).accepted
            for pan, tilt in positions
        ):
            output_fn("Limite servo non accettato: commissioning interrotto senza salvare.")
            return EXIT_NOT_READY

        camera_result = executor.test_camera(camera_factory())
        output_fn(f"Foto JPEG acquisita ({camera_result.jpeg_bytes} byte).")

        version = package_version or _version()
        commissioned = DoctorConfig(
            model_defaults=config.model_defaults,
            unit_calibration=candidate,
            commissioning=CommissioningRecord(
                status="commissioned",
                timestamp=datetime.now(timezone.utc).isoformat(),
                package_version=version,
                hardware_fingerprint=f"{platform.system()}-{platform.machine()}",
                watchdog_samples_ms=tuple(
                    round(sample * 1000.0, 3) for sample in watchdog.samples_seconds
                ),
            ),
        )
        output_fn("Configurazione proposta (non contiene credenziali):")
        output_fn(json.dumps(commissioned.to_dict(), ensure_ascii=False, indent=2))
        if input_fn("Scrivi SALVA per rendere persistente la calibrazione: ").strip() != "SALVA":
            output_fn("Configurazione non salvata.")
            return EXIT_CANCELLED
        save_config(config_path, commissioned)
        output_fn(f"Calibrazione salvata in {config_path}")
        return EXIT_READY
    finally:
        backend.stop()


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        prog="romeo-doctor",
        description="Preflight passivo e commissioning supervisionato di Romeo",
    )
    modes = result.add_mutually_exclusive_group()
    modes.add_argument("--student", action="store_true", help="preflight passivo (default)")
    modes.add_argument(
        "--commission",
        "--active",
        dest="commission",
        action="store_true",
        help="test attivi supervisionati riservati al docente",
    )
    result.add_argument("--json", action="store_true", help="output machine-readable")
    result.add_argument("--config", type=Path, default=default_config_path())
    return result


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.commission:
        if arguments.json:
            parser().error("--json non è disponibile durante il commissioning interattivo")
        from romeo.backends.factory import create_backend

        backend: Backend | None = None
        try:
            backend = create_backend("crickit", config_path=arguments.config)
            return run_commissioning(arguments.config, backend)
        except (DoctorConfigError, RuntimeError, ValueError) as error:
            print(f"[ERRORE] Commissioning non completato: {error}")
            return EXIT_ERROR
        except KeyboardInterrupt:
            print("\nCommissioning interrotto; motori fermati.")
            return EXIT_CANCELLED
        finally:
            if backend is not None:
                with suppress(Exception):
                    backend.close()

    report = run_preflight(arguments.config)
    print(render_json(report) if arguments.json else render_text(report))
    return EXIT_READY if report.ready else EXIT_NOT_READY


if __name__ == "__main__":
    raise SystemExit(main())
