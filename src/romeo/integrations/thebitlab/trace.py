"""Strict command trace used across the untrusted sandbox boundary."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from romeo.simulation.engine import SimulationEngine

TRACE_SCHEMA = "romeo.command_trace.v1"
MAX_TRACE_COMMANDS = 10_000
MAX_CAPTURE_CHARS = 100_000


@dataclass(frozen=True, slots=True)
class TraceCommand:
    operation: str
    arguments: tuple[float | int, ...]


class TraceBackend:
    """Record only public Romeo operations; it contains no scenario or grader."""

    def __init__(self, *, max_simulation_seconds: float) -> None:
        if not math.isfinite(max_simulation_seconds) or max_simulation_seconds <= 0:
            raise ValueError("max_simulation_seconds must be positive and finite")
        self.max_simulation_seconds = float(max_simulation_seconds)
        self.elapsed = 0.0
        self.commands: list[TraceCommand] = []
        self.closed = False

    def set_motor_speeds(self, left: float, right: float) -> None:
        self._append("motors", self._finite(left), self._finite(right))

    def set_camera_angles(self, pan: float, tilt: float) -> None:
        self._append("camera", self._finite(pan), self._finite(tilt))

    def set_led_color(self, red: int, green: int, blue: int) -> None:
        if any(
            isinstance(value, bool) or not isinstance(value, int)
            for value in (red, green, blue)
        ):
            raise TypeError("LED components must be integers")
        self._append("led", red, green, blue)

    def stop(self) -> None:
        self._append("stop")

    def wait(self, seconds: float) -> None:
        duration = self._finite(seconds)
        if duration < 0:
            raise ValueError("sleep duration must not be negative")
        if self.elapsed + duration > self.max_simulation_seconds + 1e-12:
            raise RuntimeError(
                f"simulated time exceeds {self.max_simulation_seconds:g} seconds"
            )
        self.elapsed += duration
        self._append("wait", duration)

    def close(self) -> None:
        if not self.closed:
            self.stop()
            self.closed = True

    def to_payload(
        self,
        *,
        stdout: str = "",
        stderr: str = "",
        student_error: str | None = None,
    ) -> dict[str, Any]:
        return {
            "schema_version": TRACE_SCHEMA,
            "commands": [
                {"operation": command.operation, "arguments": list(command.arguments)}
                for command in self.commands
            ],
            "stdout": stdout[:MAX_CAPTURE_CHARS],
            "stderr": stderr[:MAX_CAPTURE_CHARS],
            "student_error": student_error,
        }

    def _append(self, operation: str, *arguments: float | int) -> None:
        if self.closed:
            raise RuntimeError("trace backend is closed")
        if len(self.commands) >= MAX_TRACE_COMMANDS:
            raise RuntimeError(f"command trace exceeds {MAX_TRACE_COMMANDS} operations")
        self.commands.append(TraceCommand(operation, tuple(arguments)))

    @staticmethod
    def _finite(value: object) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("trace values must be numbers")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError("trace values must be finite")
        return result


def replay_trace(
    payload: object,
    engine: SimulationEngine,
    *,
    max_simulation_seconds: float,
) -> tuple[str, str, str | None]:
    """Validate untrusted trace data and replay allowed operations on a fresh engine."""

    if not isinstance(payload, dict) or payload.get("schema_version") != TRACE_SCHEMA:
        raise ValueError(f"trace schema_version must be {TRACE_SCHEMA!r}")
    commands = payload.get("commands")
    if not isinstance(commands, list) or len(commands) > MAX_TRACE_COMMANDS:
        raise ValueError("trace commands must be a bounded array")
    elapsed = 0.0
    arities = {"motors": 2, "camera": 2, "led": 3, "stop": 0, "wait": 1}
    for index, raw in enumerate(commands):
        if not isinstance(raw, dict) or set(raw) != {"operation", "arguments"}:
            raise ValueError(f"trace command {index} has invalid fields")
        operation = raw.get("operation")
        arguments = raw.get("arguments")
        if operation not in arities or not isinstance(arguments, list):
            raise ValueError(f"trace command {index} is unsupported")
        if len(arguments) != arities[operation]:
            raise ValueError(f"trace command {index} has invalid arity")
        values = tuple(_finite_number(value, index) for value in arguments)
        if operation == "motors":
            engine.set_motor_speeds(values[0], values[1])
        elif operation == "camera":
            engine.set_camera_angles(values[0], values[1])
        elif operation == "led":
            if any(not value.is_integer() for value in values):
                raise ValueError(f"trace command {index} LED values must be integers")
            engine.set_led_color(*(int(value) for value in values))
        elif operation == "stop":
            engine.stop()
        else:
            duration = values[0]
            if duration < 0 or elapsed + duration > max_simulation_seconds + 1e-12:
                raise ValueError("trace exceeds the simulated time limit")
            elapsed += duration
            engine.step(duration)
    return (
        _bounded_text(payload.get("stdout"), "stdout"),
        _bounded_text(payload.get("stderr"), "stderr"),
        _optional_error(payload.get("student_error")),
    )


def _finite_number(value: object, index: int) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"trace command {index} arguments must be numbers")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"trace command {index} arguments must be finite")
    return result


def _bounded_text(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) > MAX_CAPTURE_CHARS:
        raise ValueError(f"trace {label} must be a bounded string")
    return value


def _optional_error(value: object) -> str | None:
    if value is None:
        return None
    text = _bounded_text(value, "student_error")
    return text or None
