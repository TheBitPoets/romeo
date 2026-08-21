"""Headless command-schedule runner used by tests and future runtime adapters."""

from __future__ import annotations

import math
from dataclasses import dataclass

from romeo.simulation.engine import SimulationEngine


@dataclass(frozen=True, slots=True)
class TimedCommand:
    at: float
    command: str
    speed: float = 0.5


def run_schedule(
    engine: SimulationEngine,
    commands: list[TimedCommand],
    *,
    duration: float,
) -> SimulationEngine:
    """Run commands at exact simulated times without sleeping on the host."""

    if not math.isfinite(duration) or duration < 0.0:
        raise ValueError("duration must be a non-negative finite number")
    previous_time = 0.0
    for command in commands:
        if not math.isfinite(command.at) or command.at < previous_time or command.at > duration:
            raise ValueError("commands must be sorted and fall within the run duration")
        delta = command.at - engine.time
        if delta < -1e-9:
            raise ValueError("engine time is already past a scheduled command")
        engine.step(max(0.0, delta))
        _apply(engine, command)
        previous_time = command.at
    remaining = duration - engine.time
    if remaining < -1e-9:
        raise ValueError("engine time exceeds the requested duration")
    engine.step(max(0.0, remaining))
    return engine


def _apply(engine: SimulationEngine, command: TimedCommand) -> None:
    speed = command.speed
    actions = {
        "forward": (speed, speed),
        "backward": (-speed, -speed),
        "left": (-speed, speed),
        "right": (speed, -speed),
        "stop": (0.0, 0.0),
    }
    try:
        left, right = actions[command.command]
    except KeyError as exc:
        raise ValueError(f"unsupported command: {command.command!r}") from exc
    engine.set_motor_speeds(left, right)
