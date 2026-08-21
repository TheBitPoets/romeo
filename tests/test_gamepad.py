from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from romeo.gamepad import GamepadMapping, drive_command, run_gamepad, wheel_speeds
from romeo.network.protocol import Command


def test_dead_zone_and_cardinal_mapping() -> None:
    mapping = GamepadMapping(dead_zone=0.1, max_speed=0.8)

    assert wheel_speeds(0.05, -0.05, mapping) == (0.0, 0.0)
    assert wheel_speeds(0.0, -1.0, mapping) == pytest.approx((0.8, 0.8))
    assert wheel_speeds(1.0, 0.0, mapping) == pytest.approx((0.8, -0.8))


def test_diagonal_mapping_is_normalized() -> None:
    left, right = wheel_speeds(
        1.0,
        -1.0,
        GamepadMapping(dead_zone=0.0, max_speed=0.6),
    )

    assert left == pytest.approx(0.6)
    assert right == pytest.approx(0.0)


def test_drive_command_uses_explicit_wheel_protocol() -> None:
    command = drive_command(
        0.0,
        -1.0,
        GamepadMapping(dead_zone=0.0, max_speed=0.5),
    )

    assert command == Command("DRIVE", (0.5, 0.5))
    assert command.to_line() == "DRIVE 0.5 0.5"


def test_gamepad_stops_when_device_is_removed() -> None:
    class Sender:
        def __init__(self) -> None:
            self.commands: list[Command] = []

        def send(self, command: Command) -> str:
            self.commands.append(command)
            return "OK"

    class FakeJoystick:
        def init(self) -> None:
            return

        def get_axis(self, axis: int) -> float:
            return (0.0, -1.0)[axis]

        def get_button(self, button: int) -> bool:
            del button
            return False

    class FakeClock:
        def tick(self, updates: int) -> None:
            del updates

    events: list[list[Any]] = [[], [SimpleNamespace(type=2)]]
    pygame = SimpleNamespace(
        QUIT=1,
        JOYDEVICEREMOVED=2,
        init=lambda: None,
        quit=lambda: None,
        joystick=SimpleNamespace(
            get_count=lambda: 1,
            init=lambda: None,
            Joystick=lambda _: FakeJoystick(),
        ),
        time=SimpleNamespace(Clock=FakeClock),
        event=SimpleNamespace(get=lambda: events.pop(0)),
    )
    sender = Sender()

    run_gamepad(sender, pygame_module=pygame)

    assert sender.commands == [Command("DRIVE", (0.7, 0.7)), Command("STOP")]


def test_gamepad_quits_and_attempts_stop_when_initialization_fails() -> None:
    calls: list[str] = []

    class Sender:
        def send(self, command: Command) -> str:
            calls.append(command.name)
            return "OK"

    pygame = SimpleNamespace(
        init=lambda: calls.append("init"),
        quit=lambda: calls.append("quit"),
        joystick=SimpleNamespace(init=lambda: None, get_count=lambda: 0),
    )
    with pytest.raises(RuntimeError, match="no game controller"):
        run_gamepad(Sender(), pygame_module=pygame)
    assert calls == ["init", "STOP", "quit"]
