"""Container entrypoint that executes a submission without trusted grading data."""

from __future__ import annotations

import argparse
import ast
import contextlib
import io
import json
import os
import runpy
import sys
import time
import traceback
from pathlib import Path
from typing import Any

from romeo.backends.factory import backend_override
from romeo.easy import close as close_easy_api
from romeo.integrations.thebitlab.trace import TraceBackend

MAX_CAPTURE_CHARS = 100_000


class _BehavioralReporter:
    def __init__(self) -> None:
        self.results: dict[str, dict[str, object]] = {}

    def pytest_runtest_logreport(self, report: Any) -> None:
        if report.when not in {"setup", "call"} or (report.when == "setup" and report.passed):
            return
        name = report.nodeid.rsplit("::", 1)[-1].split("[", 1)[0]
        previous = self.results.get(name)
        passed = bool(report.passed) and (previous is None or bool(previous["passed"]))
        detail = "" if passed else str(report.longrepr)[:MAX_CAPTURE_CHARS]
        self.results[name] = {"name": name, "passed": passed, "detail": detail}


def execute_behavioral_tests(submission: Path, tests_path: Path) -> dict[str, object]:
    """Run the trusted activity checks inside the broker-owned container."""

    stdout = io.StringIO()
    stderr = io.StringIO()
    reporter = _BehavioralReporter()
    original_path = sys.path.copy()
    original_argv = sys.argv.copy()
    original_cwd = Path.cwd()
    previous_plugin_autoload = os.environ.get("PYTEST_DISABLE_PLUGIN_AUTOLOAD")
    previous_main = sys.modules.pop("main", None)
    previous_tests_module = sys.modules.pop(tests_path.stem, None)
    try:
        os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        import pytest

        sys.path.insert(0, str(submission.parent))
        os.chdir(tests_path.parent)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = pytest.main(
                [
                    tests_path.name,
                    "-q",
                    "--disable-warnings",
                    "--tb=short",
                ],
                plugins=[reporter],
            )
    finally:
        os.chdir(original_cwd)
        if previous_plugin_autoload is None:
            os.environ.pop("PYTEST_DISABLE_PLUGIN_AUTOLOAD", None)
        else:
            os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = previous_plugin_autoload
        sys.modules.pop("main", None)
        sys.modules.pop(tests_path.stem, None)
        if previous_main is not None:
            sys.modules["main"] = previous_main
        if previous_tests_module is not None:
            sys.modules[tests_path.stem] = previous_tests_module
        sys.path[:] = original_path
        sys.argv = original_argv
    tree = ast.parse(tests_path.read_text(encoding="utf-8"), filename=str(tests_path))
    names = [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    ]
    tests = [
        reporter.results.get(
            name,
            {"name": name, "passed": False, "detail": "test was not executed"},
        )
        for name in names
    ]
    return {
        "schema_version": "romeo.behavioural_result.v1",
        "exit_code": int(exit_code),
        "tests": tests,
        "stdout": stdout.getvalue()[:MAX_CAPTURE_CHARS],
        "stderr": stderr.getvalue()[:MAX_CAPTURE_CHARS],
    }


def execute_to_trace(submission: Path, *, max_simulation_seconds: float) -> dict[str, object]:
    backend = TraceBackend(max_simulation_seconds=max_simulation_seconds)
    stdout = io.StringIO()
    stderr = io.StringIO()
    student_error: str | None = None
    original_sleep = time.sleep
    original_argv = sys.argv.copy()
    result: dict[str, object] | None = None
    close_easy_api()
    time.sleep = backend.wait  # type: ignore[assignment]
    try:
        with (
            backend_override(backend),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            sys.argv = [str(submission)]
            runpy.run_path(str(submission), run_name="__main__")
    except BaseException:
        student_error = traceback.format_exc(limit=20)
    finally:
        time.sleep = original_sleep
        sys.argv = original_argv
        result = backend.to_payload(
            stdout=stdout.getvalue(),
            stderr=stderr.getvalue(),
            student_error=student_error,
        )
        close_easy_api()
    if result is None:  # pragma: no cover - defensive narrowing
        raise AssertionError("sandbox worker did not capture a trace")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path)
    parser.add_argument("--max-simulation-seconds", type=float)
    arguments = parser.parse_args()
    mode = "command-trace"
    if arguments.source is None:
        envelope = json.load(sys.stdin)
        if (
            not isinstance(envelope, dict)
            or envelope.get("schema_version") != "runtime_sandbox_worker_request.v1"
        ):
            raise SystemExit("invalid sandbox request")
        request = envelope.get("request")
        if not isinstance(request, dict) or request.get(
            "schema_version"
        ) != "romeo.sandbox_request.v1":
            raise SystemExit("invalid Romeo worker request")
        requested_mode = request.get("mode")
        if not isinstance(requested_mode, str) or requested_mode not in {
            "command-trace",
            "behavioral-tests",
        } or request.get(
            "entrypoint"
        ) != "main.py":
            raise SystemExit("unsupported sandbox request")
        mode = requested_mode
        source = Path("/submission/main.py")
        maximum = request.get("max_simulation_seconds")
        if isinstance(maximum, bool) or not isinstance(maximum, (int, float)):
            raise SystemExit("invalid simulation time limit")
    else:
        if arguments.max_simulation_seconds is None:
            parser.error("--max-simulation-seconds is required with --source")
        source = arguments.source
        maximum = arguments.max_simulation_seconds
        if mode == "behavioral-tests":
            result = execute_behavioral_tests(
                source, Path("/submission/behavioral_tests.py")
            )
        else:
            result = execute_to_trace(source, max_simulation_seconds=float(maximum))
    if arguments.source is not None:
        result = execute_to_trace(source, max_simulation_seconds=float(maximum))
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
