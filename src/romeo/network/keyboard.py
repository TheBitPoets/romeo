"""Readable, input-based keyboard controller for the first networking labs."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from typing import Protocol

from romeo.network.protocol import Command, parse_command

HELP = "W avanti | S indietro | A sinistra | D destra | SPACE stop | Q esci"

_KEY_COMMANDS = {
    "W": "FORWARD",
    "S": "BACKWARD",
    "A": "LEFT",
    "D": "RIGHT",
    "SPACE": "STOP",
    " ": "STOP",
}


class CommandSender(Protocol):
    """The small part of ``TcpClient`` needed by the keyboard UI."""

    def send(self, command: Command) -> str: ...


def command_for_key(key: str) -> Command | None:
    """Translate one student-facing key; return ``None`` for quit."""

    normalized = key.upper() if key == " " else key.strip().upper()
    if normalized == "Q":
        return None
    command = _KEY_COMMANDS.get(normalized)
    if command is None:
        raise ValueError("usa W, S, A, D, SPACE oppure Q")
    return parse_command(command)


def run_keyboard(
    client: CommandSender,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Run a portable prompt without exposing terminal-specific APIs."""

    output_fn(HELP)
    while True:
        key = input_fn("> ")
        try:
            command = command_for_key(key)
        except ValueError as error:
            output_fn(str(error))
            continue
        if command is None:
            output_fn("Controllo terminato")
            return
        output_fn(client.send(command))


def main() -> None:
    """Connect the portable keyboard prompt to a Romeo TCP server."""

    from romeo.network.client import DEFAULT_PORT, TcpClient

    parser = argparse.ArgumentParser(description="Controlla Romeo con W/S/A/D")
    parser.add_argument("host", help="Nome host o indirizzo IP di Romeo")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    arguments = parser.parse_args()
    with TcpClient(arguments.host, arguments.port) as client:
        run_keyboard(client)
