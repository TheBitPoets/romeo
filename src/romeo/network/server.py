"""Async TCP server for Romeo's deliberately small text protocol."""

from __future__ import annotations

import argparse
import asyncio
import itertools
from contextlib import suppress

from romeo.network.protocol import Command, ProtocolError, error_response, parse_command
from romeo.safety import ControllerAccessError, ControllerBusyError, SafetyBackend

MAX_COMMAND_BYTES = 1024


class TcpRobotServer:
    """Expose one safely-owned Romeo controller over newline-delimited TCP."""

    def __init__(
        self,
        backend: SafetyBackend,
        *,
        host: str = "127.0.0.1",
        port: int = 8765,
    ) -> None:
        if not 0 <= port <= 65535:
            raise ValueError("port must be between 0 and 65535")
        self.backend = backend
        self.host = host
        self.port = port
        self._server: asyncio.Server | None = None
        self._writers: set[asyncio.StreamWriter] = set()
        self._controller_ids = itertools.count(1)

    @property
    def address(self) -> tuple[str, int]:
        if self._server is None or not self._server.sockets:
            raise RuntimeError("TCP server is not running")
        host, port = self._server.sockets[0].getsockname()[:2]
        return str(host), int(port)

    async def start(self) -> tuple[str, int]:
        if self._server is not None:
            return self.address
        self._server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port,
            limit=MAX_COMMAND_BYTES + 2,
        )
        return self.address

    async def serve_forever(self) -> None:
        if self._server is None:
            await self.start()
        if self._server is None:  # pragma: no cover - narrowed by start
            raise AssertionError("server did not start")
        async with self._server:
            await self._server.serve_forever()

    async def close(self) -> None:
        server = self._server
        self._server = None
        if server is not None:
            server.close()
            await server.wait_closed()
        writers = tuple(self._writers)
        for writer in writers:
            writer.close()
        for writer in writers:
            with suppress(ConnectionError):
                await writer.wait_closed()
        self.backend.stop()

    async def _handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        self._writers.add(writer)
        controller_id = f"tcp-{next(self._controller_ids)}"
        claimed = False
        try:
            try:
                self.backend.claim_controller(controller_id)
                claimed = True
            except ControllerBusyError:
                await self._send(writer, "ERR BUSY another controller is active")
                return
            await self._send(writer, "OK ROMEO/1 READY")
            while not reader.at_eof():
                try:
                    raw_line = await reader.readline()
                except ValueError:
                    await self._send(writer, "ERR command is too long")
                    return
                if not raw_line:
                    return
                if len(raw_line) > MAX_COMMAND_BYTES:
                    await self._send(writer, "ERR command is too long")
                    return
                try:
                    line = raw_line.decode("ascii").rstrip("\r\n")
                    command = parse_command(line)
                    self._execute(controller_id, command)
                except (UnicodeDecodeError, ProtocolError, ControllerAccessError) as error:
                    await self._send(writer, error_response(error))
                    continue
                await self._send(writer, f"OK {command.name}")
        finally:
            if claimed:
                with suppress(ControllerAccessError):
                    self.backend.release_controller(controller_id)
            self._writers.discard(writer)
            writer.close()
            with suppress(ConnectionError):
                await writer.wait_closed()

    def _execute(self, controller_id: str, command: Command) -> None:
        if command.name == "PING":
            self.backend.heartbeat(controller_id)
            return
        if command.name == "LOOK":
            pan, tilt = command.arguments
            self.backend.set_camera_angles_for(controller_id, pan, tilt)
            return
        if command.name == "STOP":
            self.backend.set_motor_speeds_for(controller_id, 0.0, 0.0)
            return
        speed = command.arguments[0]
        wheel_speeds = {
            "FORWARD": (speed, speed),
            "BACKWARD": (-speed, -speed),
            "LEFT": (-speed, speed),
            "RIGHT": (speed, -speed),
        }
        left, right = wheel_speeds[command.name]
        self.backend.set_motor_speeds_for(controller_id, left, right)

    @staticmethod
    async def _send(writer: asyncio.StreamWriter, line: str) -> None:
        writer.write((line + "\n").encode("utf-8"))
        await writer.drain()


async def _run_server(host: str, port: int, backend_name: str | None) -> None:
    from romeo.backends.factory import create_backend

    selected_backend = create_backend(backend_name)
    safety = (
        selected_backend
        if isinstance(selected_backend, SafetyBackend)
        else SafetyBackend(selected_backend)
    )
    server = TcpRobotServer(safety, host=host, port=port)
    address = await server.start()
    print(f"Romeo TCP pronto su {address[0]}:{address[1]}")
    try:
        await server.serve_forever()
    finally:
        await server.close()
        safety.close()


def main() -> None:
    """Run the teaching TCP server from the command line."""

    parser = argparse.ArgumentParser(description="Server TCP didattico di Romeo")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--backend", choices=("mock", "sim", "crickit"))
    arguments = parser.parse_args()
    with suppress(KeyboardInterrupt):
        asyncio.run(_run_server(arguments.host, arguments.port, arguments.backend))
