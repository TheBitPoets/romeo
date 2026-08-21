"""Deterministic, browser-independent differential-drive simulation engine."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any

from romeo.simulation.scenario import RectangleObstacle, Scenario


@dataclass(frozen=True, slots=True)
class Pose:
    x: float
    y: float
    heading: float


@dataclass(frozen=True, slots=True)
class TrajectoryPoint:
    time: float
    x: float
    y: float
    heading: float


@dataclass(frozen=True, slots=True)
class SimulationEvent:
    sequence: int
    time: float
    type: str
    data: dict[str, Any]


class SimulationEngine:
    """Simulate normalized wheel commands using a fixed deterministic clock."""

    STATE_SCHEMA = "romeo.simulation.state.v1"

    def __init__(self, scenario: Scenario, *, integration_step: float = 0.02) -> None:
        if not math.isfinite(integration_step) or integration_step <= 0.0:
            raise ValueError("integration_step must be a positive finite number")
        self.scenario = scenario
        self.integration_step = integration_step
        self.pose = Pose(
            scenario.start_x,
            scenario.start_y,
            math.radians(scenario.start_heading_degrees),
        )
        self.left_speed = 0.0
        self.right_speed = 0.0
        self.pan_angle = 90.0
        self.tilt_angle = 90.0
        self.led_color = (0, 0, 0)
        self.time = 0.0
        self.collisions = 0
        self.closed = False
        self.trajectory: list[TrajectoryPoint] = []
        self.events: list[SimulationEvent] = []
        self._event_sequence = 0
        self._record_trajectory()
        if self._collides(self.pose):
            raise ValueError("initial robot pose collides with the world")

    @property
    def stopped(self) -> bool:
        return self.left_speed == 0.0 and self.right_speed == 0.0

    def set_motor_speeds(self, left: float, right: float) -> None:
        self._ensure_open()
        self.left_speed = self._normalized_speed(left)
        self.right_speed = self._normalized_speed(right)
        self._record_event(
            "motors_changed",
            {"left_speed": self.left_speed, "right_speed": self.right_speed},
        )

    def set_camera_angles(self, pan: float, tilt: float) -> None:
        self._ensure_open()
        if not 0.0 <= pan <= 180.0 or not 0.0 <= tilt <= 180.0:
            raise ValueError("pan and tilt must be between 0 and 180 degrees")
        self.pan_angle = float(pan)
        self.tilt_angle = float(tilt)
        self._record_event("camera_changed", {"pan": self.pan_angle, "tilt": self.tilt_angle})

    def set_led_color(self, red: int, green: int, blue: int) -> None:
        self._ensure_open()
        if any(not 0 <= value <= 255 for value in (red, green, blue)):
            raise ValueError("LED components must be between 0 and 255")
        self.led_color = (red, green, blue)
        self._record_event("led_changed", {"red": red, "green": green, "blue": blue})

    def stop(self) -> None:
        self.left_speed = 0.0
        self.right_speed = 0.0
        self._record_event("stopped", {})

    def close(self) -> None:
        if not self.closed:
            self.stop()
            self.closed = True
            self._record_event("closed", {})

    def step(self, duration: float) -> None:
        """Advance simulated time, subdividing large steps to prevent tunnelling."""

        self._ensure_open()
        if not math.isfinite(duration) or duration < 0.0:
            raise ValueError("duration must be a non-negative finite number")
        remaining = duration
        while remaining > 1e-12:
            delta = min(self.integration_step, remaining)
            self._integrate(delta)
            remaining -= delta

    def run_for(self, duration: float) -> None:
        self.step(duration)

    def reset(self) -> None:
        self._ensure_open()
        self.pose = Pose(
            self.scenario.start_x,
            self.scenario.start_y,
            math.radians(self.scenario.start_heading_degrees),
        )
        self.left_speed = 0.0
        self.right_speed = 0.0
        self.pan_angle = 90.0
        self.tilt_angle = 90.0
        self.led_color = (0, 0, 0)
        self.time = 0.0
        self.collisions = 0
        self.trajectory.clear()
        self.events.clear()
        self._event_sequence = 0
        self._record_trajectory()
        self._record_event("reset", {})

    def state(self, *, include_trajectory: bool = True) -> dict[str, Any]:
        """Return a renderer-neutral, JSON-compatible state snapshot."""

        state: dict[str, Any] = {
            "schema_version": self.STATE_SCHEMA,
            "scenario_id": self.scenario.id,
            "time": self.time,
            "running": not self.stopped,
            "closed": self.closed,
            "pose": asdict(self.pose),
            "motors": {"left": self.left_speed, "right": self.right_speed},
            "camera": {"pan": self.pan_angle, "tilt": self.tilt_angle},
            "led": {
                "red": self.led_color[0],
                "green": self.led_color[1],
                "blue": self.led_color[2],
            },
            "collisions": self.collisions,
            "world": {
                "width": self.scenario.world_width,
                "height": self.scenario.world_height,
                "robot_radius": self.scenario.robot_radius,
                "obstacles": [asdict(obstacle) for obstacle in self.scenario.obstacles],
                **self._scenario_markers(),
            },
        }
        if include_trajectory:
            state["trajectory"] = [asdict(point) for point in self.trajectory]
        return state

    def event_log(self) -> list[dict[str, Any]]:
        return [asdict(event) for event in self.events]

    def _scenario_markers(self) -> dict[str, list[dict[str, Any]]]:
        targets: list[dict[str, Any]] = []
        checkpoints: list[dict[str, Any]] = []
        for check in self.scenario.checks:
            if check.type in {"reach_position", "stop_in_zone"}:
                x = check.parameters.get("x")
                y = check.parameters.get("y")
                if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                    targets.append({"x": x, "y": y, "label": check.name})
            elif check.type == "checkpoints":
                raw_checkpoints = check.parameters.get("checkpoints")
                if isinstance(raw_checkpoints, tuple):
                    for index, item in enumerate(raw_checkpoints, start=1):
                        if isinstance(item, Mapping):
                            marker_x = item.get("x")
                            marker_y = item.get("y")
                            if isinstance(marker_x, (int, float)) and isinstance(
                                marker_y, (int, float)
                            ):
                                checkpoints.append({"x": marker_x, "y": marker_y, "label": index})
        return {"targets": targets, "checkpoints": checkpoints}

    def _integrate(self, duration: float) -> None:
        left_velocity = self.left_speed * self.scenario.max_wheel_speed
        right_velocity = self.right_speed * self.scenario.max_wheel_speed
        linear_velocity = (left_velocity + right_velocity) / 2.0
        angular_velocity = (right_velocity - left_velocity) / self.scenario.wheel_base
        heading = self.pose.heading
        new_heading = self._normalized_heading(heading + angular_velocity * duration)
        if abs(angular_velocity) < 1e-12:
            new_x = self.pose.x + linear_velocity * math.cos(heading) * duration
            new_y = self.pose.y + linear_velocity * math.sin(heading) * duration
        else:
            turn_radius = linear_velocity / angular_velocity
            new_x = self.pose.x + turn_radius * (math.sin(new_heading) - math.sin(heading))
            new_y = self.pose.y - turn_radius * (math.cos(new_heading) - math.cos(heading))
        candidate = Pose(new_x, new_y, new_heading)
        self.time += duration
        if self._collides(candidate):
            self.collisions += 1
            self.left_speed = 0.0
            self.right_speed = 0.0
            self._record_event(
                "collision",
                {"attempted_pose": asdict(candidate), "collision_count": self.collisions},
            )
        else:
            self.pose = candidate
        self._record_trajectory()

    def _collides(self, pose: Pose) -> bool:
        radius = self.scenario.robot_radius
        if (
            pose.x - radius < 0.0
            or pose.y - radius < 0.0
            or pose.x + radius > self.scenario.world_width
            or pose.y + radius > self.scenario.world_height
        ):
            return True
        return any(
            self._circle_intersects_rectangle(pose, obstacle)
            for obstacle in self.scenario.obstacles
        )

    def _circle_intersects_rectangle(self, pose: Pose, obstacle: RectangleObstacle) -> bool:
        closest_x = min(max(pose.x, obstacle.x), obstacle.x + obstacle.width)
        closest_y = min(max(pose.y, obstacle.y), obstacle.y + obstacle.height)
        distance_squared = (pose.x - closest_x) ** 2 + (pose.y - closest_y) ** 2
        return distance_squared <= self.scenario.robot_radius**2

    def _record_trajectory(self) -> None:
        self.trajectory.append(
            TrajectoryPoint(self.time, self.pose.x, self.pose.y, self.pose.heading)
        )

    def _record_event(self, event_type: str, data: dict[str, Any]) -> None:
        self._event_sequence += 1
        self.events.append(
            SimulationEvent(self._event_sequence, self.time, event_type, data.copy())
        )

    @staticmethod
    def _normalized_speed(speed: float) -> float:
        if not math.isfinite(speed) or not -1.0 <= speed <= 1.0:
            raise ValueError("wheel speed must be a finite number between -1 and 1")
        return float(speed)

    @staticmethod
    def _normalized_heading(heading: float) -> float:
        return (heading + math.pi) % (2.0 * math.pi) - math.pi

    def _ensure_open(self) -> None:
        if self.closed:
            raise RuntimeError("simulation is closed")
