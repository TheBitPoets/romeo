"""Isolated-process executor for a single deterministic Romeo submission."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import runpy
import sys
import time
import traceback
from pathlib import Path
from typing import Any

from romeo.backends.factory import backend_override
from romeo.easy import close as close_easy_api
from romeo.simulation.engine import SimulationEngine
from romeo.simulation.grading import grade
from romeo.simulation.scenario import Scenario


class SimulationTimeLimitError(RuntimeError):
    """The student program requested more simulated time than the activity allows."""


def execute_submission(
    submission: Path,
    scenario_path: Path,
    *,
    max_simulation_seconds: float,
) -> dict[str, Any]:
    scenario = Scenario.from_json(scenario_path)
    engine = SimulationEngine(scenario)
    standard_output = io.StringIO()
    standard_error = io.StringIO()
    student_error: str | None = None
    original_sleep = time.sleep
    original_argv = sys.argv.copy()
    grade_result: dict[str, Any] | None = None
    state_result: dict[str, Any] | None = None
    events_result: list[dict[str, Any]] | None = None
    close_easy_api()

    def simulated_sleep(seconds: float) -> None:
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
            raise TypeError("sleep duration must be a number")
        if seconds < 0.0:
            raise ValueError("sleep duration must not be negative")
        if engine.time + seconds > max_simulation_seconds + 1e-12:
            raise SimulationTimeLimitError(
                f"simulated time exceeds {max_simulation_seconds:g} seconds"
            )
        engine.step(float(seconds))

    time.sleep = simulated_sleep  # type: ignore[assignment]
    try:
        with (
            backend_override(engine),
            contextlib.redirect_stdout(standard_output),
            contextlib.redirect_stderr(standard_error),
        ):
            sys.argv = [str(submission)]
            runpy.run_path(str(submission), run_name="__main__")
    except BaseException:
        student_error = traceback.format_exc(limit=20)
    finally:
        time.sleep = original_sleep
        sys.argv = original_argv
        try:
            # Grade the student-visible final state before cleanup stops/closes the engine.
            grade_result = grade(engine).to_mapping()
        except Exception:
            grade_result = {
                "schema_version": "romeo.grade.v1",
                "passed": False,
                "score": 0.0,
                "checks": [],
            }
            if student_error is None:
                student_error = traceback.format_exc(limit=20)
        finally:
            state_result = engine.state()
            events_result = engine.event_log()
            close_easy_api()
    if grade_result is None:  # pragma: no cover - defensive narrowing
        raise AssertionError("grading did not produce a result")
    if state_result is None or events_result is None:  # pragma: no cover
        raise AssertionError("grading did not capture final state")
    return {
        "schema_version": "romeo.worker_result.v1",
        "student_error": student_error,
        "stdout": standard_output.getvalue(),
        "stderr": standard_error.getvalue(),
        "state": state_result,
        "events": events_result,
        "grade": grade_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--scenario", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--max-simulation-seconds", type=float, required=True)
    arguments = parser.parse_args()
    result = execute_submission(
        arguments.submission,
        arguments.scenario,
        max_simulation_seconds=arguments.max_simulation_seconds,
    )
    arguments.result.write_text(
        json.dumps(result, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
