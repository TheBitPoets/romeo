"""Optional pygame game-controller client with testable analog mapping."""

from __future__ import annotations

import argparse
import importlib
import math
from dataclasses import dataclass
from typing import Any, Protocol

from romeo.network.client import DEFAULT_PORT, TcpClient
from romeo.network.protocol import Command


class CommandSender(Protocol):
    def send(self, command: Command) -> str: ...


@dataclass(frozen=True, slots=True)
class GamepadMapping:
    horizontal_axis: int = 0
    vertical_axis: int = 1
    stop_button: int = 0
    dead_zone: float = 0.12
    max_speed: float = 0.7

    def __post_init__(self) -> None:
        if not 0.0 <= self.dead_zone < 1.0:
            raise ValueError("dead_zone must be between 0 and 1")
        if not 0.0 < self.max_speed <= 1.0:
            raise ValueError("max_speed must be greater than 0 and at most 1")


def wheel_speeds(
    x: float,
    y: float,
    mapping: GamepadMapping | None = None,
) -> tuple[float, float]:
    """Convert a joystick position to differential wheel speeds."""

    active_mapping = mapping or GamepadMapping()
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError("gamepad axes must be finite numbers")
    magnitude = min(1.0, math.hypot(x, y))
    if magnitude <= active_mapping.dead_zone:
        return 0.0, 0.0
    scaled_magnitude = (magnitude - active_mapping.dead_zone) / (
        1.0 - active_mapping.dead_zone
    )
    scale = scaled_magnitude / magnitude
    turn = max(-1.0, min(1.0, x * scale))
    forward = max(-1.0, min(1.0, -y * scale))
    left = forward + turn
    right = forward - turn
    normalization = max(1.0, abs(left), abs(right))
    return (
        left / normalization * active_mapping.max_speed,
        right / normalization * active_mapping.max_speed,
    )


def drive_command(x: float, y: float, mapping: GamepadMapping | None = None) -> Command:
    return Command("DRIVE", wheel_speeds(x, y, mapping))


def run_gamepad(
    client: CommandSender,
    *,
    mapping: GamepadMapping | None = None,
    pygame_module: Any | None = None,
    updates_per_second: int = 20,
) -> None:
    """Send analog commands and guarantee STOP on quit or controller loss."""

    if updates_per_second <= 0:
        raise ValueError("updates_per_second must be greater than zero")
    active_mapping = mapping or GamepadMapping()
    if pygame_module is None:
        try:
            pygame_api: Any = importlib.import_module("pygame")
        except ImportError as error:
            raise RuntimeError("pygame is not installed; install the 'gamepad' extra") from error
    else:
        pygame_api = pygame_module
    pygame_api.init()
    pygame_api.joystick.init()
    if pygame_api.joystick.get_count() < 1:
        pygame_api.quit()
        raise RuntimeError("no game controller found")
    joystick = pygame_api.joystick.Joystick(0)
    joystick.init()
    clock = pygame_api.time.Clock()
    previous: Command | None = None
    try:
        running = True
        while running:
            for event in pygame_api.event.get():
                if event.type in {pygame_api.QUIT, pygame_api.JOYDEVICEREMOVED}:
                    running = False
            if not running:
                break
            if joystick.get_button(active_mapping.stop_button):
                command = Command("STOP")
            else:
                command = drive_command(
                    joystick.get_axis(active_mapping.horizontal_axis),
                    joystick.get_axis(active_mapping.vertical_axis),
                    active_mapping,
                )
            if command != previous:
                client.send(command)
                previous = command
            elif command.name == "DRIVE" and command.arguments != (0.0, 0.0):
                client.send(Command("PING"))
            clock.tick(updates_per_second)
    finally:
        try:
            client.send(Command("STOP"))
        finally:
            pygame_api.quit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Controlla Romeo con un gamepad")
    parser.add_argument("host", help="Nome host o indirizzo IP di Romeo")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--max-speed", type=float, default=0.7)
    arguments = parser.parse_args()
    with TcpClient(arguments.host, arguments.port) as client:
        run_gamepad(client, mapping=GamepadMapping(max_speed=arguments.max_speed))
