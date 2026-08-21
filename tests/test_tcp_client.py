from __future__ import annotations

import socket
import threading
from collections.abc import Iterator
from contextlib import contextmanager

import pytest

from romeo.network.client import ClientError, ServerError, TcpClient
from romeo.network.keyboard import command_for_key, run_keyboard
from romeo.network.protocol import Command


@contextmanager
def local_server(responses: list[bytes]) -> Iterator[tuple[str, int, list[bytes]]]:
    received: list[bytes] = []
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)

    def serve() -> None:
        connection, _ = listener.accept()
        with connection:
            connection.sendall(responses[0])
            for response in responses[1:]:
                received.append(_receive_line(connection))
                connection.sendall(response)

    thread = threading.Thread(target=serve)
    thread.start()
    host, port = listener.getsockname()
    try:
        yield str(host), int(port), received
    finally:
        thread.join(timeout=2)
        listener.close()


def _receive_line(connection: socket.socket) -> bytes:
    data = bytearray()
    while not data.endswith(b"\n"):
        chunk = connection.recv(1024)
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


def test_client_reads_greeting_sends_command_and_closes() -> None:
    with local_server([b"READY romeo\n", b"OK moving\n"]) as (host, port, received):
        client = TcpClient(host, port)
        with client:
            assert client.greeting == "READY romeo"
            assert client.send(Command("FORWARD", (0.4,))) == "OK moving"
        assert not client.connected
    assert received == [b"FORWARD 0.4\n"]


def test_server_error_becomes_exception() -> None:
    with (
        local_server([b"READY\n", b"ERR speed rejected\n"]) as (host, port, _),
        TcpClient(host, port) as client,
        pytest.raises(ServerError, match="speed rejected"),
    ):
        client.send(Command("FORWARD", (0.5,)))


def test_send_requires_a_connection() -> None:
    with pytest.raises(ClientError, match="not connected"):
        TcpClient("localhost").send(Command("PING"))


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("w", Command("FORWARD", (0.5,))),
        ("S", Command("BACKWARD", (0.5,))),
        ("a", Command("LEFT", (0.5,))),
        ("d", Command("RIGHT", (0.5,))),
        ("SPACE", Command("STOP")),
        (" ", Command("STOP")),
        ("q", None),
    ],
)
def test_keyboard_mapping(key: str, expected: Command | None) -> None:
    assert command_for_key(key) == expected


def test_keyboard_loop_is_input_based_and_retries_invalid_keys() -> None:
    class RecordingClient:
        def __init__(self) -> None:
            self.commands: list[Command] = []

        def send(self, command: Command) -> str:
            self.commands.append(command)
            return "OK"

    entries = iter(["x", "w", "q"])
    output: list[str] = []
    client = RecordingClient()

    run_keyboard(client, input_fn=lambda _prompt: next(entries), output_fn=output.append)

    assert client.commands == [Command("FORWARD", (0.5,))]
    assert any("usa W" in line for line in output)
    assert output[-1] == "Controllo terminato"
