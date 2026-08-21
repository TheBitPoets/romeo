"""Data-driven deterministic grading for Romeo simulation scenarios."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from romeo.simulation.engine import SimulationEngine
from romeo.simulation.scenario import ScenarioCheck


@dataclass(frozen=True, slots=True)
class CheckResult:
    id: str
    name: str
    passed: bool
    detail: str
    points: float
    awarded: float


@dataclass(frozen=True, slots=True)
class GradeResult:
    passed: bool
    score: float
    checks: tuple[CheckResult, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": "romeo.grade.v1",
            "passed": self.passed,
            "score": self.score,
            "checks": [asdict(check) for check in self.checks],
        }


def grade(engine: SimulationEngine) -> GradeResult:
    results = tuple(_evaluate(check, engine) for check in engine.scenario.checks)
    available = sum(result.points for result in results)
    awarded = sum(result.awarded for result in results)
    score = round(10.0 * awarded / available, 4) if available else 10.0
    return GradeResult(all(result.passed for result in results), score, results)


def _evaluate(check: ScenarioCheck, engine: SimulationEngine) -> CheckResult:
    points = _number(check.parameters, "points", default=1.0)
    if points <= 0.0:
        raise ValueError(f"check {check.id!r} points must be greater than zero")
    evaluators = {
        "reach_position": _reach_position,
        "avoid_collisions": _avoid_collisions,
        "final_orientation": _final_orientation,
        "stop_in_zone": _stop_in_zone,
        "max_time": _max_time,
        "checkpoints": _checkpoints,
    }
    try:
        evaluator = evaluators[check.type]
    except KeyError as exc:
        raise ValueError(f"unsupported check type: {check.type!r}") from exc
    passed, detail = evaluator(check.parameters, engine)
    return CheckResult(check.id, check.name, passed, detail, points, points if passed else 0.0)


def _reach_position(parameters: Mapping[str, object], engine: SimulationEngine) -> tuple[bool, str]:
    target_x = _number(parameters, "x")
    target_y = _number(parameters, "y")
    tolerance = _number(parameters, "tolerance", default=0.1)
    distance = math.hypot(engine.pose.x - target_x, engine.pose.y - target_y)
    return distance <= tolerance, f"distance from target: {distance:.4f} m"


def _avoid_collisions(
    parameters: Mapping[str, object], engine: SimulationEngine
) -> tuple[bool, str]:
    maximum = int(_number(parameters, "max_collisions", default=0.0))
    return engine.collisions <= maximum, f"collisions: {engine.collisions} (maximum {maximum})"


def _final_orientation(
    parameters: Mapping[str, object], engine: SimulationEngine
) -> tuple[bool, str]:
    target = math.radians(_number(parameters, "degrees"))
    tolerance = math.radians(_number(parameters, "tolerance_degrees", default=5.0))
    difference = abs((engine.pose.heading - target + math.pi) % (2.0 * math.pi) - math.pi)
    return difference <= tolerance, f"orientation error: {math.degrees(difference):.2f} degrees"


def _stop_in_zone(parameters: Mapping[str, object], engine: SimulationEngine) -> tuple[bool, str]:
    reached, distance_detail = _reach_position(parameters, engine)
    passed = reached and engine.stopped
    return passed, f"{distance_detail}; stopped: {engine.stopped}"


def _max_time(parameters: Mapping[str, object], engine: SimulationEngine) -> tuple[bool, str]:
    maximum = _number(parameters, "seconds")
    return engine.time <= maximum, f"elapsed: {engine.time:.4f} s (maximum {maximum:.4f} s)"


def _checkpoints(parameters: Mapping[str, object], engine: SimulationEngine) -> tuple[bool, str]:
    raw_points = parameters.get("checkpoints")
    if (
        not isinstance(raw_points, Sequence)
        or isinstance(raw_points, (str, bytes))
        or not raw_points
    ):
        raise ValueError("checkpoints check requires a non-empty 'checkpoints' list")
    tolerance = _number(parameters, "tolerance", default=0.1)
    trajectory_index = 0
    for checkpoint_index, raw_point in enumerate(raw_points):
        if not isinstance(raw_point, Mapping):
            raise ValueError("each checkpoint must be an object")
        x = _number(raw_point, "x")
        y = _number(raw_point, "y")
        while trajectory_index < len(engine.trajectory):
            point = engine.trajectory[trajectory_index]
            trajectory_index += 1
            if math.hypot(point.x - x, point.y - y) <= tolerance:
                break
        else:
            return False, f"checkpoint {checkpoint_index + 1} not reached in order"
    return True, f"{len(raw_points)} checkpoints reached in order"


def _number(parameters: Mapping[str, object], key: str, *, default: float | None = None) -> float:
    value = parameters.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"parameter {key!r} must be a finite number")
    return float(value)
