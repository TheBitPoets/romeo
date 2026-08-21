"""TheBitLab runtime ABI adapter for the deterministic Romeo simulator."""

from __future__ import annotations

import ast
import importlib.util
import json
import math
import os
import re
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

from romeo.integrations.thebitlab.trace import TRACE_SCHEMA, replay_trace
from romeo.simulation.engine import SimulationEngine
from romeo.simulation.grading import grade
from romeo.simulation.scenario import Scenario

RUNTIME_ID = "romeo-sim"
PLUGIN_VERSION = "0.2.0"
MAX_SUBMISSION_BYTES = 1_000_000
MAX_CAPTURE_CHARS = 100_000
SANDBOX_PLAN_SCHEMA = "runtime_sandbox_plan.v1"
SANDBOX_RESULT_SCHEMA = "runtime_sandbox_result.v1"
_PINNED_IMAGE_RE = re.compile(r"^[a-z0-9][a-z0-9./_-]*@sha256:[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class RuntimeContext:
    activity_path: Path
    workspace: Path
    config_path: Path
    scenario_path: Path
    submission_path: Path
    timeout_seconds: int
    max_simulation_seconds: float
    stdout_checks: tuple[StdoutCheck, ...]
    behavioral_tests_path: Path | None
    behavioral_entrypoints: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StdoutCheck:
    name: str
    contains: str
    points: float


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
                "sandbox-plan.v1",
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
            "metadata": {
                "interactive_available": self._web_available(),
                "execution_isolation": "process-only",
                "untrusted_submissions_supported": False,
                "sandbox_broker_available": self._sandbox_image() is not None,
            },
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
        environment = self._child_environment()
        environment["ROMEO_SCENARIO"] = str(context.scenario_path)
        command = [
            sys.executable,
            "-I",
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

        try:
            run_directory = self._create_run_directory(context.workspace)
        except (OSError, ValueError) as error:
            return self._execution_result(
                "invalid_payload",
                started_at,
                detail=f"unsafe artifact directory: {error}",
            )
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
        environment = self._child_environment()
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
            checks, score, checks_passed = self._test_results(result, context.stdout_checks)
            student_error = result.get("student_error")
            passed = not student_error and checks_passed
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
                metadata={
                    "score": score,
                    "artifacts": artifacts,
                    "authoritative": False,
                    "execution_isolation": "process-only",
                },
            )
        except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
            return self._execution_result(
                "failed",
                started_at,
                stderr=infrastructure_stderr,
                detail=f"invalid worker result: {error}",
                tests=[{"name": "runtime worker", "passed": False, "detail": str(error)}],
            )

    def prepare_sandbox(self, request: dict[str, Any]) -> dict[str, Any]:
        """Prepare a minimal broker plan without exposing scenario or grading policy."""

        context = self._request_context(request)
        image = self._sandbox_image()
        if image is None:
            raise ValueError(
                "ROMEO_SANDBOX_IMAGE must name an immutable OCI image by sha256 digest"
            )
        behavioral = context.behavioral_tests_path is not None
        worker_schema = "romeo.behavioural_result.v1" if behavioral else TRACE_SCHEMA
        inputs = [
            {
                "source": "submission",
                "artifact_id": self._submission_artifact_id(request, context.submission_path),
                "target": "main.py",
            }
        ]
        if context.behavioral_tests_path is not None:
            inputs.append(
                {
                    "source": "activity",
                    "path": context.behavioral_tests_path.relative_to(
                        context.activity_path.parent
                    ).as_posix(),
                    "target": "behavioral_tests.py",
                }
            )
        return {
            "schema_version": SANDBOX_PLAN_SCHEMA,
            "profile": {
                "image": image,
                "platform": "linux/amd64",
                "worker_schema": worker_schema,
            },
            "inputs": inputs,
            "worker_request": {
                "schema_version": "romeo.sandbox_request.v1",
                "mode": "behavioral-tests" if behavioral else "command-trace",
                "entrypoint": "main.py",
                "max_simulation_seconds": context.max_simulation_seconds,
                "entrypoints": list(context.behavioral_entrypoints),
            },
        }

    def finalize_sandbox(
        self,
        request: dict[str, Any],
        sandbox_result: dict[str, Any],
    ) -> dict[str, Any]:
        """Replay an untrusted command trace and grade only on the trusted host."""

        started_at = time.monotonic()
        try:
            context = self._request_context(request)
            if context.behavioral_tests_path is not None:
                return self._finalize_behavioral(context, sandbox_result, started_at)
            payload = self._sandbox_payload(sandbox_result, TRACE_SCHEMA)
            engine = SimulationEngine(Scenario.from_json(context.scenario_path))
            stdout, stderr, student_error = replay_trace(
                payload,
                engine,
                max_simulation_seconds=context.max_simulation_seconds,
            )
            grade_result = grade(engine).to_mapping()
            result = {
                "schema_version": "romeo.worker_result.v1",
                "student_error": student_error,
                "stdout": stdout,
                "stderr": stderr,
                "state": engine.state(),
                "events": engine.event_log(),
                "grade": grade_result,
            }
            run_directory = self._create_run_directory(context.workspace)
            artifacts = self._write_artifacts(context, run_directory, result)
            checks, score, checks_passed = self._test_results(result, ())
            passed = student_error is None and checks_passed
            return self._execution_result(
                "passed" if passed else "failed",
                started_at,
                stdout=stdout,
                stderr=(f"{stderr}\n{student_error or ''}").strip(),
                detail=(
                    "mission completed in the TheBitLab sandbox"
                    if passed
                    else "mission requirements not met"
                ),
                tests=checks,
                metadata={
                    "score": score,
                    "artifacts": artifacts,
                    "authoritative": True,
                    "execution_isolation": "thebitlab-sandbox",
                },
            )
        except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
            return self._execution_result(
                "invalid_payload",
                started_at,
                detail=f"sandbox result rejected: {error}",
            )

    def _finalize_behavioral(
        self,
        context: RuntimeContext,
        sandbox_result: dict[str, Any],
        started_at: float,
    ) -> dict[str, Any]:
        payload = self._sandbox_payload(sandbox_result, "romeo.behavioural_result.v1")
        if payload.get("schema_version") != "romeo.behavioural_result.v1":
            raise ValueError("behavioral result has an unsupported schema")
        raw_tests = payload.get("tests")
        if not isinstance(raw_tests, list):
            raise TypeError("behavioral result tests must be an array")
        expected = self._behavioral_test_names(context.behavioral_tests_path)
        tests: list[dict[str, Any]] = []
        names: list[str] = []
        for index, raw in enumerate(raw_tests):
            if not isinstance(raw, dict):
                raise TypeError(f"behavioral test {index} must be an object")
            name = raw.get("name")
            passed = raw.get("passed")
            detail = raw.get("detail", "")
            if not isinstance(name, str) or not isinstance(passed, bool):
                raise TypeError(f"behavioral test {index} has invalid fields")
            if not isinstance(detail, str) or len(detail) > MAX_CAPTURE_CHARS:
                raise ValueError(f"behavioral test {index} detail is invalid")
            names.append(name)
            tests.append({"name": name, "passed": passed, "detail": detail})
        if tuple(names) != expected:
            raise ValueError("behavioral result does not match the trusted test manifest")
        passed = bool(tests) and all(test["passed"] for test in tests)
        score = round(10.0 * sum(test["passed"] for test in tests) / len(tests), 4)
        run_directory = self._create_run_directory(context.workspace)
        result_path = run_directory / "result.json"
        result_path.write_text(
            json.dumps({"passed": passed, "score": score, "tests": tests}, indent=2),
            encoding="utf-8",
        )
        artifact = {
            "id": "result",
            "path": result_path.relative_to(context.workspace).as_posix(),
            "media_type": "application/json",
            "size": result_path.stat().st_size,
        }
        return self._execution_result(
            "passed" if passed else "failed",
            started_at,
            stdout=self._bounded_payload_text(payload, "stdout"),
            stderr=self._bounded_payload_text(payload, "stderr"),
            detail="behavioral contract verified" if passed else "behavioral tests failed",
            tests=tests,
            metadata={
                "score": score,
                "artifacts": [artifact],
                "authoritative": True,
                "execution_isolation": "thebitlab-sandbox",
            },
        )

    def close(self, session_id: str) -> None:
        with self._sessions_lock:
            process = self._sessions.pop(session_id, None)
        if process is not None:
            self._terminate(process)

    @staticmethod
    def _sandbox_payload(result: object, worker_schema: str) -> dict[str, Any]:
        if not isinstance(result, dict) or result.get("schema_version") != SANDBOX_RESULT_SCHEMA:
            raise ValueError(f"sandbox result schema must be {SANDBOX_RESULT_SCHEMA!r}")
        if result.get("status") != "completed" or result.get("worker_schema") != worker_schema:
            raise ValueError("sandbox worker did not complete with the expected schema")
        payload = result.get("payload")
        if not isinstance(payload, dict):
            raise TypeError("sandbox payload must be an object")
        return payload

    @staticmethod
    def _behavioral_test_names(path: Path | None) -> tuple[str, ...]:
        if path is None:
            raise ValueError("behavioral test path is missing")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        names = tuple(
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
        if not names or len(names) != len(set(names)):
            raise ValueError("behavioral test manifest must contain unique tests")
        return names

    @staticmethod
    def _bounded_payload_text(payload: dict[str, Any], key: str) -> str:
        value = payload.get(key, "")
        if not isinstance(value, str) or len(value) > MAX_CAPTURE_CHARS:
            raise ValueError(f"behavioral {key} must be a bounded string")
        return value

    @staticmethod
    def _sandbox_image() -> str | None:
        image = os.environ.get("ROMEO_SANDBOX_IMAGE", "").strip().lower()
        return image if _PINNED_IMAGE_RE.fullmatch(image) else None

    @staticmethod
    def _submission_artifact_id(request: dict[str, Any], path: Path) -> str:
        workspace = Path(str(request["paths"]["workspace"])).resolve()
        relative = path.relative_to(workspace).as_posix()
        for artifact in request["submission_artifacts"]:
            if isinstance(artifact, dict) and artifact.get("path") == relative:
                artifact_id = artifact.get("id")
                if isinstance(artifact_id, str) and artifact_id:
                    return artifact_id
        raise ValueError("submission artifact id could not be resolved")

    def _request_context(self, request: dict[str, Any]) -> RuntimeContext:
        if not isinstance(request, dict) or request.get("schema_version") != "runtime_request.v1":
            raise ValueError("request schema_version must be 'runtime_request.v1'")
        if request.get("runtime_id") != RUNTIME_ID:
            raise ValueError(f"runtime_id must be {RUNTIME_ID!r}")
        paths = request.get("paths")
        if not isinstance(paths, dict):
            raise TypeError("paths must be an object")
        activity_path = self._absolute_file(paths.get("activity"), "paths.activity")
        activity_root = activity_path.parent
        workspace = self._absolute_directory(paths.get("workspace"), "paths.workspace")
        config_path = self._contained_file(paths.get("config"), activity_root, "paths.config")
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict) or config.get("schema_version") != "romeo.thebitlab.v1":
            raise ValueError("config schema_version must be 'romeo.thebitlab.v1'")
        scenario_relative = self._safe_relative(config.get("scenario"), "config.scenario")
        scenario_path = self._resolved_within(
            config_path.parent,
            scenario_relative,
            activity_root,
        )
        if not scenario_path.is_file():
            raise ValueError("configured scenario file does not exist")
        Scenario.from_json(scenario_path)
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
        stdout_checks = self._stdout_checks(config.get("stdout_checks", []))
        behavioral_path: Path | None = None
        behavioral_entrypoints: tuple[str, ...] = ()
        behavioral = config.get("behavioral_tests")
        if behavioral is not None:
            if not isinstance(behavioral, dict):
                raise TypeError("behavioral_tests must be an object")
            if behavioral.get("execution_boundary") not in {
                None,
                "thebitlab-sandbox-broker",
            }:
                raise ValueError("behavioral_tests requires the TheBitLab sandbox broker")
            relative = self._safe_relative(behavioral.get("path"), "behavioral_tests.path")
            behavioral_path = self._resolved_within(
                config_path.parent,
                relative,
                activity_root,
            )
            if not behavioral_path.is_file():
                raise ValueError("configured behavioral test file does not exist")
            raw_entrypoints = behavioral.get("entrypoints")
            if not isinstance(raw_entrypoints, list) or not raw_entrypoints:
                raise ValueError("behavioral_tests.entrypoints must be a non-empty array")
            if any(
                not isinstance(name, str) or not name.isidentifier()
                for name in raw_entrypoints
            ):
                raise ValueError("behavioral test entrypoints must be Python identifiers")
            behavioral_entrypoints = tuple(raw_entrypoints)
        return RuntimeContext(
            activity_path,
            workspace,
            config_path,
            scenario_path,
            submission_path,
            timeout,
            float(maximum),
            stdout_checks,
            behavioral_path,
            behavioral_entrypoints,
        )

    def _write_artifacts(
        self,
        context: RuntimeContext,
        run_directory: Path,
        result: dict[str, Any],
    ) -> list[dict[str, Any]]:
        self._assert_run_directory(context.workspace, run_directory)
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
            self._assert_run_directory(context.workspace, run_directory)
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
        self._assert_run_directory(context.workspace, run_directory)
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
    def _create_run_directory(workspace: Path) -> Path:
        workspace = workspace.resolve()
        current = workspace
        for segment in (".romeo", "artifacts"):
            current = current / segment
            if current.exists() and (current.is_symlink() or not current.is_dir()):
                raise ValueError(f"{current.name} must be a real directory")
            current.mkdir(exist_ok=True)
            if not current.resolve().is_relative_to(workspace):
                raise ValueError("artifact directory escapes the workspace")
        run_directory = current / uuid4().hex
        run_directory.mkdir(exist_ok=False)
        RomeoRuntimePlugin._assert_run_directory(workspace, run_directory)
        return run_directory

    @staticmethod
    def _assert_run_directory(workspace: Path, run_directory: Path) -> None:
        workspace = workspace.resolve()
        if run_directory.is_symlink() or not run_directory.resolve().is_relative_to(workspace):
            raise ValueError("artifact run directory escapes the workspace")

    @staticmethod
    def _child_environment() -> dict[str, str]:
        """Pass only platform startup variables, never arbitrary host secrets."""

        allowed = (
            "SYSTEMROOT",
            "WINDIR",
            "COMSPEC",
            "PATHEXT",
            "TEMP",
            "TMP",
            "LANG",
            "LC_ALL",
        )
        environment = {name: os.environ[name] for name in allowed if name in os.environ}
        environment["PYTHONUTF8"] = "1"
        return environment

    @staticmethod
    def _test_results(
        result: dict[str, Any], stdout_checks: tuple[StdoutCheck, ...]
    ) -> tuple[list[dict[str, Any]], float, bool]:
        grade_checks = result["grade"]["checks"]
        tests = [
            {
                "name": str(check["name"]),
                "passed": bool(check["passed"]),
                "detail": str(check.get("detail", "")),
            }
            for check in grade_checks
        ]
        stdout = str(result.get("stdout", ""))
        output_results: list[tuple[bool, float]] = []
        for check in stdout_checks:
            check_passed = check.contains in stdout
            output_results.append((check_passed, check.points))
            tests.append(
                {
                    "name": check.name,
                    "passed": check_passed,
                    "detail": (
                        f"output contains {check.contains!r}"
                        if check_passed
                        else f"expected output marker {check.contains!r}"
                    ),
                }
            )
        if result.get("student_error"):
            tests.insert(
                0,
                {
                    "name": "student program",
                    "passed": False,
                    "detail": "the program raised an exception",
                },
            )
        available = sum(float(check["points"]) for check in grade_checks) + sum(
            points for _, points in output_results
        )
        awarded = sum(float(check["awarded"]) for check in grade_checks) + sum(
            points for passed, points in output_results if passed
        )
        score = round(10.0 * awarded / available, 4) if available else 10.0
        return tests, score, all(test["passed"] for test in tests)

    @staticmethod
    def _stdout_checks(value: object) -> tuple[StdoutCheck, ...]:
        if not isinstance(value, list):
            raise TypeError("stdout_checks must be an array")
        checks: list[StdoutCheck] = []
        for index, raw in enumerate(value):
            if not isinstance(raw, dict):
                raise TypeError(f"stdout_checks[{index}] must be an object")
            name = raw.get("name")
            contains = raw.get("contains")
            points = raw.get("points", 1.0)
            if not isinstance(name, str) or not name.strip():
                raise ValueError(f"stdout_checks[{index}].name must be non-empty")
            if not isinstance(contains, str) or not contains:
                raise ValueError(f"stdout_checks[{index}].contains must be non-empty")
            if (
                isinstance(points, bool)
                or not isinstance(points, (int, float))
                or not math.isfinite(points)
                or points <= 0
            ):
                raise ValueError(f"stdout_checks[{index}].points must be positive")
            checks.append(StdoutCheck(name.strip(), contains, float(points)))
        return tuple(checks)

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
    def _absolute_file(value: object, label: str) -> Path:
        if not isinstance(value, str):
            raise TypeError(f"{label} must be a path string")
        path = Path(value)
        if not path.is_absolute() or not path.is_file():
            raise ValueError(f"{label} must be an existing absolute file")
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
