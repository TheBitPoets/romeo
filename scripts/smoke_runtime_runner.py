"""Smoke-test the Romeo runtime image through its production ENTRYPOINT."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def worker_envelope(mode: str, worker_schema: str, inputs: list[dict[str, str]]) -> str:
    return json.dumps(
        {
            "schema_version": "runtime_sandbox_worker_request.v1",
            "worker_schema": worker_schema,
            "inputs": inputs,
            "request": {
                "schema_version": "romeo.sandbox_request.v1",
                "mode": mode,
                "entrypoint": "main.py",
                "max_simulation_seconds": 5,
                "entrypoints": ["double"] if mode == "behavioral-tests" else [],
            },
        }
    )


def run_worker(image: str, submission: Path, envelope: str) -> dict[str, Any]:
    completed = subprocess.run(
        [
            "docker",
            "run",
            "-i",
            "--rm",
            "--network",
            "none",
            "--user",
            "runner",
            "--read-only",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--pids-limit",
            "128",
            "--memory",
            "256m",
            "--cpus",
            "1",
            "-v",
            f"{submission.resolve()}:/submission:ro",
            "--tmpfs",
            "/thebitlab-work:rw,exec,nosuid,nodev,mode=1777,size=64m",
            "-e",
            "TMPDIR=/thebitlab-work",
            "-w",
            "/submission",
            image,
        ],
        input=envelope,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"runtime runner exited with {completed.returncode}: {completed.stderr}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"runtime runner returned invalid JSON: {completed.stdout!r}") from error
    if not isinstance(result, dict):
        raise RuntimeError("runtime runner result must be a JSON object")
    return result


def smoke_command_trace(image: str, root: Path) -> None:
    submission = root / "command-trace"
    submission.mkdir()
    (submission / "main.py").write_text(
        "from romeo.easy import forward, stop\n"
        "from time import sleep\n"
        "forward(0.4)\nsleep(1)\nstop()\n",
        encoding="utf-8",
    )
    result = run_worker(
        image,
        submission,
        worker_envelope(
            "command-trace",
            "romeo.command_trace.v1",
            [{"source": "submission", "id": "main", "path": "main.py"}],
        ),
    )
    if result.get("schema_version") != "romeo.command_trace.v1":
        raise RuntimeError(f"unexpected command trace result: {result!r}")
    if not result.get("commands"):
        raise RuntimeError("command trace smoke did not execute any command")


def smoke_behavioral_tests(image: str, root: Path) -> None:
    submission = root / "behavioral-tests"
    submission.mkdir()
    (submission / "main.py").write_text(
        "def double(value):\n    return value * 2\n", encoding="utf-8"
    )
    (submission / "behavioral_tests.py").write_text(
        "from main import double\n\n"
        "def test_double_uses_its_argument():\n"
        "    assert double(4) == 8\n",
        encoding="utf-8",
    )
    result = run_worker(
        image,
        submission,
        worker_envelope(
            "behavioral-tests",
            "romeo.behavioural_result.v1",
            [
                {"source": "submission", "id": "main", "path": "main.py"},
                {
                    "source": "activity",
                    "id": "runtime/behavioral_tests.py",
                    "path": "behavioral_tests.py",
                },
            ],
        ),
    )
    if result.get("schema_version") != "romeo.behavioural_result.v1":
        raise RuntimeError(f"unexpected behavioral result: {result!r}")
    expected = {"name": "test_double_uses_its_argument", "passed": True, "detail": ""}
    if result.get("exit_code") != 0 or result.get("tests") != [expected]:
        raise RuntimeError(f"behavioral smoke did not execute its test: {result!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    arguments = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="romeo-runtime-smoke-") as temporary:
        root = Path(temporary)
        smoke_command_trace(arguments.image, root)
        smoke_behavioral_tests(arguments.image, root)
    print("Romeo runtime command-trace and behavioral-tests smoke passed")


if __name__ == "__main__":
    main()
