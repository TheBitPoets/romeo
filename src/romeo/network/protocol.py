"""Small, line-based command protocol used in the networking lessons."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal, cast

CommandName = Literal[
    "FORWARD",
    "BACKWARD",
    "LEFT",
    "RIGHT",
    "DRIVE",
    "STOP",
    "LOOK",
    "PING",
]

_MOVEMENT_COMMANDS = frozenset({"FORWARD", "BACKWARD", "LEFT", "RIGHT"})
_COMMANDS = _MOVEMENT_COMMANDS | {"DRIVE", "STOP", "LOOK", "PING"}
DEFAULT_SPEED = 0.5


class ProtocolError(ValueError):
    """A command is not valid Romeo protocol input."""


@dataclass(frozen=True, slots=True)
class Command:
    """A validated command and its numeric arguments."""

    name: CommandName
    arguments: tuple[float, ...] = ()

    def to_line(self) -> str:
        """Serialize the command without its terminating newline."""

        parts = [self.name, *(format(value, "g") for value in self.arguments)]
        return " ".join(parts)


def parse_command(line: str) -> Command:
    """Parse and validate one command line.

    Command words are case-insensitive so students can type them naturally.  A
    line may not contain embedded newlines: framing remains the responsibility
    of the TCP layer.
    """

    if "\n" in line or "\r" in line:
        raise ProtocolError("command must contain exactly one line")
    parts = line.split()
    if not parts:
        raise ProtocolError("empty command")

    raw_name = parts[0].upper()
    if raw_name not in _COMMANDS:
        raise ProtocolError(f"unknown command {parts[0]!r}")
    name = cast(CommandName, raw_name)
    raw_arguments = parts[1:]

    if name in _MOVEMENT_COMMANDS:
        if len(raw_arguments) > 1:
            raise ProtocolError(f"{name} accepts zero or one speed")
        speed = DEFAULT_SPEED if not raw_arguments else _number(raw_arguments[0], "speed")
        if not 0.0 <= speed <= 1.0:
            raise ProtocolError("speed must be between 0 and 1")
        return Command(name, (speed,))

    if name == "LOOK":
        if len(raw_arguments) != 2:
            raise ProtocolError("LOOK requires pan and tilt angles")
        pan = _number(raw_arguments[0], "pan")
        tilt = _number(raw_arguments[1], "tilt")
        if not 0.0 <= pan <= 180.0 or not 0.0 <= tilt <= 180.0:
            raise ProtocolError("pan and tilt must be between 0 and 180 degrees")
        return Command(name, (pan, tilt))

    if name == "DRIVE":
        if len(raw_arguments) != 2:
            raise ProtocolError("DRIVE requires left and right wheel speeds")
        left = _number(raw_arguments[0], "left wheel speed")
        right = _number(raw_arguments[1], "right wheel speed")
        if not -1.0 <= left <= 1.0 or not -1.0 <= right <= 1.0:
            raise ProtocolError("wheel speeds must be between -1 and 1")
        return Command(name, (left, right))

    if raw_arguments:
        raise ProtocolError(f"{name} does not accept arguments")
    return Command(name)


def error_response(error: Exception | str) -> str:
    """Create the single-line error response sent to a protocol client."""

    detail = str(error).replace("\r", " ").replace("\n", " ").strip()
    return f"ERR {detail or 'invalid command'}"


def _number(text: str, label: str) -> float:
    try:
        value = float(text)
    except ValueError as error:
        raise ProtocolError(f"{label} must be a number") from error
    if not math.isfinite(value):
        raise ProtocolError(f"{label} must be finite")
    return value
