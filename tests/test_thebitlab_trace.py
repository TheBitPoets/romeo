from __future__ import annotations

import io
import json
import sys

import pytest

from romeo.integrations.thebitlab import sandbox_worker
from romeo.integrations.thebitlab.sandbox_worker import (
    execute_behavioral_tests,
    execute_to_trace,
)
from romeo.integrations.thebitlab.trace import MAX_TRACE_COMMANDS, replay_trace
from romeo.simulation import Scenario, SimulationEngine


def engine() -> SimulationEngine:
    return SimulationEngine(
        Scenario.from_mapping({"schema_version": "romeo.scenario.v1", "id": "trace"})
    )


def run_main_from_stdin(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    submission: object,
    request: dict[str, object],
) -> dict[str, object]:
    envelope = {
        "schema_version": "runtime_sandbox_worker_request.v1",
        "worker_schema": "unused-by-worker",
        "inputs": [],
        "request": request,
    }
    monkeypatch.chdir(submission)
    monkeypatch.setattr(sys, "argv", ["sandbox-worker"])
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(envelope)))

    sandbox_worker.main()

    return json.loads(capsys.readouterr().out)


def test_main_dispatches_command_trace_from_broker_stdin(
    tmp_path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "main.py").write_text(
        "from romeo.easy import forward, stop\n"
        "from time import sleep\n"
        "forward(0.4)\nsleep(1)\nstop()\n",
        encoding="utf-8",
    )

    result = run_main_from_stdin(
        monkeypatch,
        capsys,
        tmp_path,
        {
            "schema_version": "romeo.sandbox_request.v1",
            "mode": "command-trace",
            "entrypoint": "main.py",
            "max_simulation_seconds": 5,
            "entrypoints": [],
        },
    )

    assert result["schema_version"] == "romeo.command_trace.v1"
    assert [command["operation"] for command in result["commands"]] == [
        "motors",
        "wait",
        "stop",
    ]


def test_main_dispatches_behavioral_tests_from_broker_stdin(
    tmp_path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "main.py").write_text(
        "def double(value):\n    return value * 2\n", encoding="utf-8"
    )
    (tmp_path / "behavioral_tests.py").write_text(
        "from main import double\n\n"
        "def test_double_uses_its_argument():\n"
        "    assert double(4) == 8\n",
        encoding="utf-8",
    )

    result = run_main_from_stdin(
        monkeypatch,
        capsys,
        tmp_path,
        {
            "schema_version": "romeo.sandbox_request.v1",
            "mode": "behavioral-tests",
            "entrypoint": "main.py",
            "max_simulation_seconds": 5,
            "entrypoints": ["double"],
        },
    )

    assert result["schema_version"] == "romeo.behavioural_result.v1"
    assert result["exit_code"] == 0
    assert result["tests"] == [
        {"name": "test_double_uses_its_argument", "passed": True, "detail": ""}
    ]


def test_legacy_source_dispatches_command_trace_once(
    tmp_path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "main.py"
    source.write_text("print('legacy')\n", encoding="utf-8")
    calls = 0

    def execute_once(path, *, max_simulation_seconds):
        nonlocal calls
        calls += 1
        assert path == source
        assert max_simulation_seconds == 5.0
        return {"schema_version": "romeo.command_trace.v1"}

    monkeypatch.setattr(sandbox_worker, "execute_to_trace", execute_once)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "sandbox-worker",
            "--source",
            str(source),
            "--max-simulation-seconds",
            "5",
        ],
    )

    sandbox_worker.main()

    assert calls == 1
    assert json.loads(capsys.readouterr().out)["schema_version"] == (
        "romeo.command_trace.v1"
    )


def test_sandbox_worker_contains_no_scenario_or_grade(tmp_path) -> None:
    source = tmp_path / "main.py"
    source.write_text(
        "from romeo.easy import forward, stop\n"
        "from time import sleep\n"
        "forward(0.4)\nsleep(1)\nstop()\n",
        encoding="utf-8",
    )

    trace = execute_to_trace(source, max_simulation_seconds=5)

    assert set(trace) == {"schema_version", "commands", "stdout", "stderr", "student_error"}
    assert [item["operation"] for item in trace["commands"]] == ["motors", "wait", "stop"]


def test_replay_is_deterministic_and_uses_a_fresh_engine() -> None:
    trace = {
        "schema_version": "romeo.command_trace.v1",
        "commands": [
            {"operation": "motors", "arguments": [0.4, 0.4]},
            {"operation": "wait", "arguments": [1.0]},
            {"operation": "stop", "arguments": []},
        ],
        "stdout": "hello",
        "stderr": "",
        "student_error": None,
    }
    first = engine()
    second = engine()

    replay_trace(trace, first, max_simulation_seconds=5)
    replay_trace(trace, second, max_simulation_seconds=5)

    assert first.state() == second.state()
    assert first.event_log() == second.event_log()


@pytest.mark.parametrize(
    "command",
    [
        {"operation": "unknown", "arguments": []},
        {"operation": "wait", "arguments": [float("nan")]},
        {"operation": "motors", "arguments": [0.2]},
        {"operation": "stop", "arguments": [], "grade": True},
    ],
)
def test_replay_rejects_malformed_or_privileged_commands(command: dict[str, object]) -> None:
    trace = {
        "schema_version": "romeo.command_trace.v1",
        "commands": [command],
        "stdout": "",
        "stderr": "",
        "student_error": None,
    }

    with pytest.raises(ValueError):
        replay_trace(trace, engine(), max_simulation_seconds=5)


def test_replay_rejects_resource_exhaustion() -> None:
    trace = {
        "schema_version": "romeo.command_trace.v1",
        "commands": [{"operation": "stop", "arguments": []}] * (MAX_TRACE_COMMANDS + 1),
        "stdout": "",
        "stderr": "",
        "student_error": None,
    }

    with pytest.raises(ValueError, match="bounded"):
        replay_trace(trace, engine(), max_simulation_seconds=5)


def test_behavioral_worker_executes_named_contract_without_stdout_markers(tmp_path) -> None:
    source = tmp_path / "main.py"
    checks = tmp_path / "behavioral_tests.py"
    source.write_text("def double(value):\n    return value * 2\n", encoding="utf-8")
    checks.write_text(
        "import pytest\n"
        "from main import double\n\n"
        "@pytest.mark.parametrize('value', [2, 5])\n"
        "def test_uses_different_inputs(value):\n"
        "    assert double(value) == value * 2\n",
        encoding="utf-8",
    )

    result = execute_behavioral_tests(source, checks)
    if result["exit_code"] != 0:
        pytest.fail(str(result["stdout"]))

    assert result["schema_version"] == "romeo.behavioural_result.v1"
    assert result["tests"] == [
        {"name": "test_uses_different_inputs", "passed": True, "detail": ""}
    ], result
