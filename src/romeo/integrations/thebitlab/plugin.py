"""TheBitLab runtime ABI adapter for the deterministic Romeo simulator."""

from __future__ import annotations

import importlib.util
import json
import math
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from uuid import uuid4

RUNTIME_ID = "romeo-sim"
PLUGIN_VERSION = "0.1.0"
MAX_SUBMISSION_BYTES = 1_000_000
MAX_CAPTURE_CHARS = 100_000


@dataclass(frozen=True, slots=True)
class RuntimeContext:
    activity: Path
    workspace: Path
    config_path: Path
    scenario_path: Path
    submission_path: Path
    timeout_seconds: int
    max_simulation_seconds: float


class RomeoRuntimePlugin:
    """Duck-typed plugin implementing runtime_plugin.v1 without core imports."""

    def __init__(self) -> None:
        self._sessions: dict[str, subprocess.Popen[bytes]] = {}
        self._sessions_lock = threading.Lock()

    def describe(self) -> dict[str, Any]:
        return {
            "schema_version": "runtime_descriptor.v1",
            "runtime_id": RUNTIME_ID,
            "display_name": "Romeo 2D Simulator",
            "plugin_version": PLUGIN_VERSION,
            "api_version": "runtime_plugin.v1",
            "capabilities": [
                "interactive-launch",
                "headless-run",
                "deterministic-grade",
                "artifact-collect",
            ],
            "vendor": "TheBitLab",
            "homepage": "https://github.com/TheBitPoets/romeo",
        }

    def probe(self) -> dict[str, Any]:
        return {
            "schema_version": "runtime_probe.v1",
            "available": True,
            "version": PLUGIN_VERSION,
            "detail": "deterministic headless simulator available",
            "metadata": {"interactive_available": self._web_available()},
        }

    def launch(self, request: dict[str, Any]) -> dict[str, Any]:
        try:
            context = self._request_context(request)
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
            return self._launch_result("invalid_payload", detail=str(error))
        if not self._web_available():
            return self._launch_result(
                "unavailable",
                detail="install the Romeo 'web' extra for interactive launch",
            )
        session_id = uuid4().hex
        port = self._available_port()
        endpoint = f"http://127.0.0.1:{port}/"
        environment = os.environ.copy()
        environment["ROMEO_SCENARIO"] = str(context.scenario_path)
        environment["PYTHONUTF8"] = "1"
        command = [
            sys.executable,
            "-m",
            "uvicorn",
            "romeo.web.app:create_app",
            "--factory",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--log-level",
            "warning",
        ]
        try:
            process = subprocess.Popen(
                command,
                cwd=context.workspace,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except OSError as error:
            return self._launch_result("error", detail=f"viewer failed to start: {error}")
        if not self._wait_for_endpoint(endpoint, process):
            self._terminate(process)
            return self._launch_result("error", detail="viewer did not become ready")
        with self._sessions_lock:
            self._sessions[session_id] = process
        return self._launch_result(
            "started",
            session_id=session_id,
            endpoint=endpoint,
            metadata={"scenario": context.scenario_path.name},
        )

    def run(self, request: dict[str, Any]) -> dict[str, Any]:
        started_at = time.monotonic()
        try:
            context = self._request_context(request)
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
            return self._execution_result(
                "invalid_payload",
                started_at,
                detail=str(error),
            )

        run_directory = context.workspace / ".romeo" / "artifacts" / uuid4().hex
        run_directory.mkdir(parents=True, exist_ok=False)
        worker_result_path = run_directory / "worker-result.json"
        command = [
            sys.executable,
            "-I",
            "-m",
            "romeo.integrations.thebitlab.worker",
            "--submission",
            str(context.submission_path),
            "--scenario",
            str(context.scenario_path),
            "--result",
            str(worker_result_path),
            "--max-simulation-seconds",
            str(context.max_simulation_seconds),
        ]
        environment = os.environ.copy()
        environment["PYTHONUTF8"] = "1"
        try:
            completed = subprocess.run(
                command,
                cwd=context.workspace,
                env=environment,
                capture_output=True,
                timeout=context.timeout_seconds,
                check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except subprocess.TimeoutExpired as error:
            return self._execution_result(
                "timeout",
                started_at,
                stdout=self._decoded(error.stdout),
                stderr=self._decoded(error.stderr),
                detail=f"submission exceeded {context.timeout_seconds} seconds",
            )
        except OSError as error:
            return self._execution_result(
                "runner_unavailable",
                started_at,
                detail=f"worker could not start: {error}",
            )

        infrastructure_stderr = self._decoded(completed.stderr)
        if completed.returncode != 0 or not worker_result_path.is_file():
            return self._execution_result(
                "failed",
                started_at,
                stdout=self._decoded(completed.stdout),
                stderr=infrastructure_stderr,
                detail=f"worker exited with code {completed.returncode}",
                tests=[
                    {
                        "name": "runtime worker",
                        "passed": False,
                        "detail": infrastructure_stderr,
                    }
                ],
            )
        try:
            result = json.loads(worker_result_path.read_text(encoding="utf-8"))
            if result.get("schema_version") != "romeo.worker_result.v1":
                raise ValueError("worker returned an unsupported result schema")
            artifacts = self._write_artifacts(context, run_directory, result)
            checks = self._test_results(result)
            student_error = result.get("student_error")
            grade_result = result["grade"]
            passed = not student_error and bool(grade_result["passed"])
            stderr = str(result.get("stderr", ""))
            if student_error:
                stderr = f"{stderr}\n{student_error}".strip()
            if infrastructure_stderr:
                stderr = f"{stderr}\n{infrastructure_stderr}".strip()
            return self._execution_result(
                "passed" if passed else "failed",
                started_at,
                stdout=str(result.get("stdout", ""))[:MAX_CAPTURE_CHARS],
                stderr=stderr[:MAX_CAPTURE_CHARS],
                detail="mission completed" if passed else "mission requirements not met",
                tests=checks,
                metadata={"score": float(grade_result["score"]), "artifacts": artifacts},
            )
        except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
            return self._execution_result(
                "failed",
                started_at,
                stderr=infrastructure_stderr,
                detail=f"invalid worker result: {error}",
                tests=[{"name": "runtime worker", "passed": False, "detail": str(error)}],
            )

    def close(self, session_id: str) -> None:
        with self._sessions_lock:
            process = self._sessions.pop(session_id, None)
        if process is not None:
            self._terminate(process)

    def _request_context(self, request: dict[str, Any]) -> RuntimeContext:
        if not isinstance(request, dict) or request.get("schema_version") != "runtime_request.v1":
            raise ValueError("request schema_version must be 'runtime_request.v1'")
        if request.get("runtime_id") != RUNTIME_ID:
            raise ValueError(f"runtime_id must be {RUNTIME_ID!r}")
        paths = request.get("paths")
        if not isinstance(paths, dict):
            raise TypeError("paths must be an object")
        activity = self._absolute_directory(paths.get("activity"), "paths.activity")
        workspace = self._absolute_directory(paths.get("workspace"), "paths.workspace")
        config_path = self._contained_file(paths.get("config"), activity, "paths.config")
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict) or config.get("schema_version") != "romeo.thebitlab.v1":
            raise ValueError("config schema_version must be 'romeo.thebitlab.v1'")
        scenario_relative = self._safe_relative(config.get("scenario"), "config.scenario")
        scenario_path = self._resolved_within(config_path.parent, scenario_relative, activity)
        if not scenario_path.is_file():
            raise ValueError("configured scenario file does not exist")
        artifact_id = config.get("submission_artifact_id", "main")
        if not isinstance(artifact_id, str) or not artifact_id:
            raise ValueError("submission_artifact_id must be a non-empty string")
        artifacts = request.get("submission_artifacts")
        if not isinstance(artifacts, list):
            raise TypeError("submission_artifacts must be an array")
        artifact = next(
            (
                item
                for item in artifacts
                if isinstance(item, dict) and item.get("id") == artifact_id
            ),
            None,
        )
        if artifact is None:
            raise ValueError(f"submission artifact {artifact_id!r} is missing")
        submission_relative = self._safe_relative(artifact.get("path"), "artifact.path")
        submission_path = self._resolved_within(workspace, submission_relative, workspace)
        if not submission_path.is_file():
            raise ValueError("required submission file does not exist")
        if submission_path.stat().st_size > MAX_SUBMISSION_BYTES:
            raise ValueError("submission file is too large")
        timeout = request.get("timeout_seconds", 30)
        if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("timeout_seconds must be a positive integer")
        maximum = config.get("max_simulation_seconds", 60.0)
        if (
            isinstance(maximum, bool)
            or not isinstance(maximum, (int, float))
            or not math.isfinite(maximum)
            or maximum <= 0
        ):
            raise ValueError("max_simulation_seconds must be a positive number")
        return RuntimeContext(
            activity,
            workspace,
            config_path,
            scenario_path,
            submission_path,
            timeout,
            float(maximum),
        )

    def _write_artifacts(
        self,
        context: RuntimeContext,
        run_directory: Path,
        result: dict[str, Any],
    ) -> list[dict[str, Any]]:
        state = dict(result["state"])
        trajectory = state.pop("trajectory", [])
        files = {
            "result": ("result.json", result["grade"], "application/json"),
            "trajectory": ("trajectory.json", trajectory, "application/json"),
            "events": ("events.json", result["events"], "application/json"),
            "final-state": ("final-state.json", state, "application/json"),
        }
        artifacts: list[dict[str, Any]] = []
        for artifact_id, (filename, content, media_type) in files.items():
            path = run_directory / filename
            path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
            artifacts.append(
                {
                    "id": artifact_id,
                    "path": path.relative_to(context.workspace).as_posix(),
                    "media_type": media_type,
                    "size": path.stat().st_size,
                }
            )
        manifest_path = run_directory / "artifact-manifest.json"
        manifest_relative = manifest_path.relative_to(context.workspace).as_posix()
        manifest = {
            "schema_version": "romeo.artifacts.v1",
            "artifacts": artifacts,
        }
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        artifacts.append(
            {
                "id": "manifest",
                "path": manifest_relative,
                "media_type": "application/json",
                "size": manifest_path.stat().st_size,
            }
        )
        return artifacts

    @staticmethod
    def _test_results(result: dict[str, Any]) -> list[dict[str, Any]]:
        tests = [
            {
                "name": str(check["name"]),
                "passed": bool(check["passed"]),
                "detail": str(check.get("detail", "")),
            }
            for check in result["grade"]["checks"]
        ]
        if result.get("student_error"):
            tests.insert(
                0,
                {
                    "name": "student program",
                    "passed": False,
                    "detail": "the program raised an exception",
                },
            )
        return tests

    @staticmethod
    def _safe_relative(value: object, label: str) -> PurePosixPath:
        if not isinstance(value, str) or not value or "\\" in value:
            raise ValueError(f"{label} must be a safe relative POSIX path")
        segments = value.split("/")
        if any(segment in {"", ".", ".."} for segment in segments):
            raise ValueError(f"{label} must be a safe relative POSIX path")
        path = PurePosixPath(value)
        if path.is_absolute():
            raise ValueError(f"{label} must be a safe relative POSIX path")
        if ":" in path.parts[0]:
            raise ValueError(f"{label} must be a safe relative POSIX path")
        return path

    @staticmethod
    def _absolute_directory(value: object, label: str) -> Path:
        if not isinstance(value, str):
            raise TypeError(f"{label} must be a path string")
        path = Path(value)
        if not path.is_absolute() or not path.is_dir():
            raise ValueError(f"{label} must be an existing absolute directory")
        return path.resolve()

    @staticmethod
    def _contained_file(value: object, parent: Path, label: str) -> Path:
        if not isinstance(value, str):
            raise TypeError(f"{label} must be a path string")
        path = Path(value)
        if not path.is_absolute():
            raise ValueError(f"{label} must be absolute")
        resolved = path.resolve()
        if not resolved.is_relative_to(parent) or not resolved.is_file():
            raise ValueError(f"{label} must be an existing file inside the activity")
        return resolved

    @staticmethod
    def _resolved_within(base: Path, relative: PurePosixPath, boundary: Path) -> Path:
        resolved = base.joinpath(*relative.parts).resolve()
        if not resolved.is_relative_to(boundary):
            raise ValueError("resolved path escapes its allowed directory")
        return resolved

    @staticmethod
    def _execution_result(
        status: str,
        started_at: float,
        *,
        tests: list[dict[str, Any]] | None = None,
        stdout: str = "",
        stderr: str = "",
        detail: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "schema_version": "runtime_execution.v1",
            "status": status,
            "tests": tests or [],
            "stdout": stdout[:MAX_CAPTURE_CHARS],
            "stderr": stderr[:MAX_CAPTURE_CHARS],
            "detail": detail,
            "duration_ms": max(0, int((time.monotonic() - started_at) * 1000)),
            "metadata": metadata or {},
        }

    @staticmethod
    def _launch_result(
        status: str,
        *,
        session_id: str | None = None,
        endpoint: str | None = None,
        detail: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {
            "schema_version": "runtime_launch.v1",
            "status": status,
            "detail": detail,
            "metadata": metadata or {},
        }
        if session_id is not None:
            result["session_id"] = session_id
        if endpoint is not None:
            result["endpoint"] = endpoint
        return result

    @staticmethod
    def _decoded(value: bytes | str | None) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value[:MAX_CAPTURE_CHARS]
        return value.decode("utf-8", errors="replace")[:MAX_CAPTURE_CHARS]

    @staticmethod
    def _web_available() -> bool:
        return (
            importlib.util.find_spec("fastapi") is not None
            and importlib.util.find_spec("uvicorn") is not None
        )

    @staticmethod
    def _available_port() -> int:
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            return int(listener.getsockname()[1])

    @staticmethod
    def _wait_for_endpoint(endpoint: str, process: subprocess.Popen[bytes]) -> bool:
        deadline = time.monotonic() + 5.0
        status_url = f"{endpoint.rstrip('/')}/api/status"
        while time.monotonic() < deadline and process.poll() is None:
            try:
                with urllib.request.urlopen(status_url, timeout=0.2) as response:
                    return int(response.status) == 200
            except OSError:
                time.sleep(0.05)
        return False

    @staticmethod
    def _terminate(process: subprocess.Popen[bytes]) -> None:
        if process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3.0)
