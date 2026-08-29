"""Passive Romeo hardware preflight built from injectable checks."""

from __future__ import annotations

import hmac
import importlib.metadata
import ipaddress
import os
import platform
import socket
import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Protocol

from romeo.backends.base import Backend
from romeo.doctor.config import DoctorConfigError, load_config
from romeo.doctor.identity import (
    UnitIdentifierProvider,
    fingerprint_unit_identifier,
    is_unit_fingerprint,
    read_raspberry_unit_identifier,
)
from romeo.doctor.models import CheckResult, DiagnosticReport, DoctorConfig
from romeo.safety import SafetyBackend


class CameraProbe(Protocol):
    @property
    def available(self) -> bool: ...

    def close(self) -> None: ...


BackendFactory = Callable[[str], Backend]
CameraFactory = Callable[[], CameraProbe]
NetworkProbe = Callable[[], list[str]]
ServerProbe = Callable[[str, int, float], bool]


def _package_version() -> str:
    return importlib.metadata.version("thebitlab-romeo")


def _backend_factory(name: str, config_path: str | Path) -> Backend:
    from romeo.backends.factory import create_backend

    return create_backend(name, config_path=config_path)


def _camera_factory() -> CameraProbe:
    from romeo.camera.picamera2 import Picamera2CameraService

    return Picamera2CameraService()


def _network_addresses() -> list[str]:
    addresses: set[str] = set()
    for result in socket.getaddrinfo(socket.gethostname(), None):
        raw_address = result[4][0]
        if not isinstance(raw_address, str):
            continue
        address = raw_address.split("%", 1)[0]
        try:
            parsed = ipaddress.ip_address(address)
        except ValueError:
            continue
        if not parsed.is_loopback and not parsed.is_unspecified:
            addresses.add(address)

    # Raspberry Pi OS commonly maps the local hostname to 127.0.1.1 in
    # /etc/hosts.  A route lookup finds the address of the actual interface
    # without sending a UDP packet or depending on an external service.
    route_probes = (
        (socket.AF_INET, ("192.0.2.1", 9)),
        (socket.AF_INET6, ("2001:db8::1", 9, 0, 0)),
    )
    for family, target in route_probes:
        try:
            with socket.socket(family, socket.SOCK_DGRAM) as probe:
                probe.connect(target)
                raw_address = probe.getsockname()[0]
        except OSError:
            continue
        address = raw_address.split("%", 1)[0]
        try:
            parsed = ipaddress.ip_address(address)
        except ValueError:
            continue
        if not parsed.is_loopback and not parsed.is_unspecified:
            addresses.add(address)
    return sorted(addresses)


def _server_probe(host: str, port: int, timeout: float) -> bool:
    with socket.create_connection((host, port), timeout=timeout):
        return True


def _skipped(check_id: str, detail: str) -> CheckResult:
    return CheckResult(check_id, "skipped", detail)


def _calibration_checks(config: DoctorConfig, package_version: str | None) -> list[CheckResult]:
    calibration = config.unit_calibration
    if calibration is None:
        return [
            CheckResult("calibration", "failed", "Romeo non è ancora stato collaudato."),
        ]
    recorded_version = config.commissioning.package_version
    if config.commissioning.status not in {"commissioned", "ready"}:
        calibration_result = CheckResult(
            "calibration", "failed", "Il commissioning non risulta completato."
        )
    elif recorded_version and package_version and recorded_version != package_version:
        calibration_result = CheckResult(
            "calibration",
            "failed",
            "Romeo è cambiato dopo il commissioning; il docente deve ricontrollarlo.",
            {"commissioned_package": recorded_version, "installed_package": package_version},
        )
    else:
        calibration_result = CheckResult(
            "calibration", "passed", "Calibrazione del singolo esemplare valida."
        )
    return [calibration_result]


def _unit_identity_check(
    config: DoctorConfig | None,
    unit_identifier_provider: UnitIdentifierProvider,
) -> CheckResult:
    if config is None or config.unit_calibration is None:
        return CheckResult(
            "unit_identity",
            "failed",
            "Identità del singolo Romeo non registrata da un commissioning valido.",
        )
    recorded = config.commissioning.hardware_fingerprint
    if not is_unit_fingerprint(recorded):
        return CheckResult(
            "unit_identity",
            "failed",
            "Fingerprint del singolo Romeo assente o non valido; rifare il commissioning.",
        )
    assert isinstance(recorded, str)
    try:
        current = fingerprint_unit_identifier(unit_identifier_provider())
    except Exception as error:
        return CheckResult(
            "unit_identity",
            "failed",
            "Impossibile verificare che la calibrazione appartenga a questo Romeo.",
            {"error": type(error).__name__},
        )
    matches = hmac.compare_digest(recorded, current)
    return CheckResult(
        "unit_identity",
        "passed" if matches else "failed",
        "Calibrazione associata a questo esemplare."
        if matches
        else "La calibrazione appartiene a un altro esemplare Romeo.",
        (
            {"fingerprint": current}
            if matches
            else {
                "recorded_fingerprint": recorded,
                "current_fingerprint": current,
            }
        ),
    )


def run_preflight(
    config_path: str | Path,
    *,
    environ: Mapping[str, str] | None = None,
    package_version_fn: Callable[[], str] = _package_version,
    backend_factory: BackendFactory | None = None,
    camera_factory: CameraFactory = _camera_factory,
    network_probe: NetworkProbe = _network_addresses,
    server_probe: ServerProbe = _server_probe,
    i2c_exists: Callable[[Path], bool] = Path.exists,
    unit_identifier_provider: UnitIdentifierProvider = read_raspberry_unit_identifier,
) -> DiagnosticReport:
    """Run checks that do not move motors or servo and return a stable report."""

    environment = os.environ if environ is None else environ
    checks: list[CheckResult] = []
    python_ok = sys.version_info >= (3, 10)
    checks.append(
        CheckResult(
            "python",
            "passed" if python_ok else "failed",
            "Versione Python supportata." if python_ok else "Serve Python 3.10 o più recente.",
            {"version": platform.python_version(), "executable": sys.executable},
        )
    )

    installed_version: str | None = None
    try:
        installed_version = package_version_fn()
        checks.append(
            CheckResult(
                "package", "passed", "Package Romeo installato.", {"version": installed_version}
            )
        )
    except importlib.metadata.PackageNotFoundError:
        checks.append(CheckResult("package", "failed", "Package thebitlab-romeo non installato."))
    except Exception as error:
        checks.append(
            CheckResult(
                "package",
                "failed",
                "Impossibile leggere la versione di Romeo.",
                type(error).__name__,
            )
        )

    config: DoctorConfig | None = None
    try:
        config = load_config(config_path)
        checks.extend(_calibration_checks(config, installed_version))
    except DoctorConfigError as error:
        checks.extend(
            [
                CheckResult(
                    "calibration",
                    "failed",
                    "Il file di calibrazione non è valido.",
                    type(error).__name__,
                ),
                _skipped("watchdog", "Calibrazione non leggibile."),
                _skipped("speed_limit", "Calibrazione non leggibile."),
            ]
        )
    checks.append(_unit_identity_check(config, unit_identifier_provider))

    selected_backend = environment.get("ROMEO_BACKEND", "mock").strip().lower()
    hardware_selected = selected_backend == "crickit"
    safety_backend: SafetyBackend | None = None
    checks.append(
        CheckResult(
            "backend",
            "passed" if hardware_selected else "failed",
            "Backend CRICKIT selezionato."
            if hardware_selected
            else "Il backend selezionato non controlla il robot reale.",
            {"selected": selected_backend},
        )
    )

    if hardware_selected:
        i2c_ok = i2c_exists(Path("/dev/i2c-1"))
        checks.append(
            CheckResult(
                "i2c",
                "passed" if i2c_ok else "failed",
                "Bus I2C disponibile." if i2c_ok else "Bus I2C non disponibile.",
                {"device": "/dev/i2c-1"},
            )
        )
        backend: Backend | None = None
        try:
            backend = (
                backend_factory("crickit")
                if backend_factory is not None
                else _backend_factory("crickit", config_path)
            )
            safety_ok = isinstance(backend, SafetyBackend)
            if isinstance(backend, SafetyBackend):
                safety_backend = backend
            checks.append(
                CheckResult(
                    "crickit",
                    "passed" if safety_ok else "failed",
                    "CRICKIT raggiungibile con protezioni attive."
                    if safety_ok
                    else "CRICKIT raggiungibile ma il backend safety non è attivo.",
                )
            )
        except Exception as error:
            checks.append(
                CheckResult(
                    "crickit", "failed", "CRICKIT non raggiungibile.", type(error).__name__
                )
            )
        finally:
            if backend is not None:
                try:
                    backend.close()
                except Exception:
                    checks.append(
                        CheckResult(
                            "crickit_close",
                            "failed",
                            "CRICKIT non ha confermato lo stop durante la chiusura.",
                        )
                    )
    else:
        checks.extend(
            [
                _skipped("i2c", "Richiede il backend crickit."),
                _skipped("crickit", "Backend hardware non selezionato."),
            ]
        )

    existing_ids = {check.id for check in checks}
    calibration = config.unit_calibration if config is not None else None
    if calibration is None:
        if "watchdog" not in existing_ids:
            checks.append(_skipped("watchdog", "Serve prima una calibrazione valida."))
        if "speed_limit" not in existing_ids:
            checks.append(_skipped("speed_limit", "Serve prima una calibrazione valida."))
    elif safety_backend is None:
        checks.extend(
            [
                _skipped("watchdog", "SafetyBackend hardware non disponibile."),
                _skipped("speed_limit", "SafetyBackend hardware non disponibile."),
            ]
        )
    else:
        assert config is not None
        effective_speed = safety_backend.max_speed
        speed_safe = effective_speed <= calibration.speed_limit
        checks.append(
            CheckResult(
                "speed_limit",
                "passed" if speed_safe else "failed",
                "Limite effettivo non supera la calibrazione."
                if speed_safe
                else "Il limite effettivo supera il valore collaudato.",
                {
                    "configured": calibration.speed_limit,
                    "effective": effective_speed,
                },
            )
        )
        effective_timeout = safety_backend.command_timeout
        samples = config.commissioning.watchdog_samples_ms
        timeout_safe = effective_timeout <= calibration.watchdog_timeout
        allowed_latency_ms = (
            calibration.watchdog_timeout
            + min(0.1, calibration.watchdog_timeout / 4.0)
            + 0.1
        ) * 1000.0
        measurements_safe = bool(samples) and max(samples) <= allowed_latency_ms
        watchdog_safe = timeout_safe and measurements_safe
        checks.append(
            CheckResult(
                "watchdog",
                "passed" if watchdog_safe else "failed",
                "Watchdog misurato e timeout effettivo non superiore alla calibrazione."
                if watchdog_safe
                else "Watchdog non misurato o timeout effettivo meno conservativo.",
                {
                    "configured_seconds": calibration.watchdog_timeout,
                    "effective_seconds": effective_timeout,
                    "samples_ms": list(samples),
                    "minimum_ms": min(samples) if samples else None,
                    "maximum_ms": max(samples) if samples else None,
                    "mean_ms": sum(samples) / len(samples) if samples else None,
                    "allowed_maximum_ms": allowed_latency_ms,
                },
            )
        )

    camera: CameraProbe | None = None
    try:
        camera = camera_factory()
        available = camera.available
        checks.append(
            CheckResult(
                "camera",
                "passed" if available else "failed",
                "Servizio Picamera2 inizializzato; apertura e foto non provate."
                if available
                else "Camera non disponibile.",
            )
        )
    except Exception as error:
        checks.append(
            CheckResult("camera", "failed", "Camera non disponibile.", type(error).__name__)
        )
    finally:
        if camera is not None:
            try:
                camera.close()
            except Exception:
                checks.append(
                    CheckResult(
                        "camera_close",
                        "warning",
                        "La camera non si è chiusa correttamente.",
                    )
                )

    try:
        addresses = network_probe()
        checks.append(
            CheckResult(
                "network",
                "passed" if addresses else "failed",
                "Rete disponibile." if addresses else "Nessun indirizzo di rete disponibile.",
                {"address_count": len(addresses)},
            )
        )
    except Exception as error:
        checks.append(
            CheckResult(
                "network",
                "failed",
                "Impossibile verificare la rete.",
                type(error).__name__,
            )
        )

    server_host = environment.get("ROMEO_DOCTOR_SERVER_HOST")
    server_port = environment.get("ROMEO_DOCTOR_SERVER_PORT")
    if not server_host and not server_port:
        checks.append(_skipped("server", "Nessun server Romeo configurato per il probe."))
    elif not server_host or not server_port or not server_port.isdigit():
        checks.append(CheckResult("server", "failed", "Configurazione probe server incompleta."))
    else:
        try:
            reachable = server_probe(server_host, int(server_port), 0.5)
            checks.append(
                CheckResult(
                    "server",
                    "passed" if reachable else "failed",
                    "Server Romeo raggiungibile."
                    if reachable
                    else "Server Romeo non raggiungibile.",
                )
            )
        except Exception as error:
            checks.append(
                CheckResult(
                    "server",
                    "failed",
                    "Server Romeo non raggiungibile.",
                    type(error).__name__,
                )
            )

    blocking = {
        "python",
        "package",
        "calibration",
        "unit_identity",
        "backend",
        "i2c",
        "crickit",
        "camera",
        "network",
        "crickit_close",
        "watchdog",
        "speed_limit",
    }
    ready = all(check.status == "passed" for check in checks if check.id in blocking)
    hardware = {
        "backend": selected_backend,
        "machine": platform.machine(),
        "system": platform.system(),
    }
    calibration_payload = calibration.to_dict() if calibration is not None else {}
    if calibration_payload and config is not None:
        calibration_payload["watchdog_samples_ms"] = list(
            config.commissioning.watchdog_samples_ms
        )
    return DiagnosticReport(
        status="ready" if ready else "preflight_failed",
        ready=ready,
        checks=tuple(checks),
        calibration=calibration_payload,
        hardware=hardware,
    )
