"""Data-driven scenario definitions for Romeo's deterministic simulator."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType

SCENARIO_SCHEMA = "romeo.scenario.v1"


def _object(value: object, location: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{location} must be an object")
    for key in value:
        if not isinstance(key, str):
            raise ValueError(f"{location} keys must be strings")
    return value


def _sequence(value: object, location: str) -> Sequence[object]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ValueError(f"{location} must be an array")
    return value


def _text(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location} must be a non-empty string")
    return value


def _number(value: object, location: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{location} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{location} must be finite")
    if positive and result <= 0:
        raise ValueError(f"{location} must be greater than zero")
    return result


def _freeze_json(value: object, location: str) -> object:
    """Validate and freeze a JSON-compatible value."""
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"{location} numbers must be finite")
        return value
    if isinstance(value, Mapping):
        frozen: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{location} keys must be strings")
            frozen[key] = _freeze_json(item, f"{location}.{key}")
        return MappingProxyType(frozen)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return tuple(_freeze_json(item, f"{location}[{index}]") for index, item in enumerate(value))
    raise ValueError(f"{location} must contain only JSON-compatible values")


@dataclass(frozen=True, slots=True)
class RectangleObstacle:
    """An axis-aligned rectangular obstacle, measured in metres."""

    x: float
    y: float
    width: float
    height: float


@dataclass(frozen=True, slots=True)
class ScenarioCheck:
    """A declarative grading check interpreted by the grading layer."""

    id: str
    name: str
    type: str
    parameters: Mapping[str, object] = field(default_factory=lambda: MappingProxyType({}))


@dataclass(frozen=True, slots=True)
class Scenario:
    """A fully validated, immutable simulation scenario."""

    schema_version: str
    id: str
    world_width: float = 4.0
    world_height: float = 3.0
    start_x: float = 0.5
    start_y: float = 0.5
    start_heading_degrees: float = 0.0
    robot_radius: float = 0.12
    wheel_base: float = 0.18
    max_wheel_speed: float = 0.5
    obstacles: tuple[RectangleObstacle, ...] = ()
    checks: tuple[ScenarioCheck, ...] = ()

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, object]) -> Scenario:
        """Build and validate a scenario from a decoded JSON object."""
        data = _object(mapping, "scenario")
        schema_version = _text(data.get("schema_version"), "schema_version")
        if schema_version != SCENARIO_SCHEMA:
            raise ValueError(f"schema_version must be exactly {SCENARIO_SCHEMA!r}")

        scenario_id = _text(data.get("id"), "id")
        world_width = _number(data.get("world_width", 4.0), "world_width", positive=True)
        world_height = _number(data.get("world_height", 3.0), "world_height", positive=True)
        robot_radius = _number(data.get("robot_radius", 0.12), "robot_radius", positive=True)
        wheel_base = _number(data.get("wheel_base", 0.18), "wheel_base", positive=True)
        max_wheel_speed = _number(
            data.get("max_wheel_speed", 0.5), "max_wheel_speed", positive=True
        )
        start_x = _number(data.get("start_x", 0.5), "start_x")
        start_y = _number(data.get("start_y", 0.5), "start_y")
        start_heading = _number(data.get("start_heading_degrees", 0.0), "start_heading_degrees")

        if 2 * robot_radius > world_width or 2 * robot_radius > world_height:
            raise ValueError("robot_radius is too large for the world")
        if not robot_radius <= start_x <= world_width - robot_radius:
            raise ValueError("start_x places the robot outside world bounds")
        if not robot_radius <= start_y <= world_height - robot_radius:
            raise ValueError("start_y places the robot outside world bounds")

        obstacles = cls._parse_obstacles(data.get("obstacles", ()), world_width, world_height)
        checks = cls._parse_checks(data.get("checks", ()))
        return cls(
            schema_version=schema_version,
            id=scenario_id,
            world_width=world_width,
            world_height=world_height,
            start_x=start_x,
            start_y=start_y,
            start_heading_degrees=start_heading,
            robot_radius=robot_radius,
            wheel_base=wheel_base,
            max_wheel_speed=max_wheel_speed,
            obstacles=obstacles,
            checks=checks,
        )

    @classmethod
    def from_json(cls, path: str | Path) -> Scenario:
        """Load a UTF-8 JSON scenario file."""
        with Path(path).open(encoding="utf-8") as source:
            decoded: object = json.load(source)
        return cls.from_mapping(_object(decoded, "scenario"))

    @staticmethod
    def _parse_obstacles(
        value: object, world_width: float, world_height: float
    ) -> tuple[RectangleObstacle, ...]:
        obstacles: list[RectangleObstacle] = []
        for index, raw in enumerate(_sequence(value, "obstacles")):
            location = f"obstacles[{index}]"
            item = _object(raw, location)
            obstacle = RectangleObstacle(
                x=_number(item.get("x"), f"{location}.x"),
                y=_number(item.get("y"), f"{location}.y"),
                width=_number(item.get("width"), f"{location}.width", positive=True),
                height=_number(item.get("height"), f"{location}.height", positive=True),
            )
            if obstacle.x < 0 or obstacle.y < 0:
                raise ValueError(f"{location} must start inside world bounds")
            if obstacle.x + obstacle.width > world_width:
                raise ValueError(f"{location} extends beyond world_width")
            if obstacle.y + obstacle.height > world_height:
                raise ValueError(f"{location} extends beyond world_height")
            obstacles.append(obstacle)
        return tuple(obstacles)

    @staticmethod
    def _parse_checks(value: object) -> tuple[ScenarioCheck, ...]:
        checks: list[ScenarioCheck] = []
        ids: set[str] = set()
        for index, raw in enumerate(_sequence(value, "checks")):
            location = f"checks[{index}]"
            item = _object(raw, location)
            check_id = _text(item.get("id"), f"{location}.id")
            if check_id in ids:
                raise ValueError(f"duplicate check id {check_id!r}")
            ids.add(check_id)
            parameters = _object(item.get("parameters", {}), f"{location}.parameters")
            frozen_parameters = _freeze_json(parameters, f"{location}.parameters")
            if not isinstance(frozen_parameters, Mapping):  # pragma: no cover - guaranteed above
                raise AssertionError("parameters did not freeze to a mapping")
            checks.append(
                ScenarioCheck(
                    id=check_id,
                    name=_text(item.get("name"), f"{location}.name"),
                    type=_text(item.get("type"), f"{location}.type"),
                    parameters=frozen_parameters,
                )
            )
        return tuple(checks)
