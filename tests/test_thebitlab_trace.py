from __future__ import annotations

import pytest

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
