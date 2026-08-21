"""Synchronous client for Romeo's teaching-oriented TCP protocol."""

from __future__ import annotations

import socket
from types import TracebackType

from romeo.network.protocol import Command

DEFAULT_PORT = 8765
MAX_LINE_BYTES = 1024


class ClientError(RuntimeError):
    """The server connection or response was not usable."""


class ServerError(ClientError):
    """The server rejected a command."""


class TcpClient:
    """A small blocking TCP client suitable for introductory examples."""

    def __init__(self, host: str, port: int = DEFAULT_PORT, *, timeout: float = 5.0) -> None:
        if not host:
            raise ValueError("host must not be empty")
        if not 1 <= port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.host = host
        self.port = port
        self.timeout = timeout
        self.greeting: str | None = None
        self._socket: socket.socket | None = None
        self._received = bytearray()

    @property
    def connected(self) -> bool:
        return self._socket is not None

    def connect(self) -> str:
        """Connect, read the server greeting and return it."""

        if self._socket is not None:
            if self.greeting is None:  # pragma: no cover - internal invariant
                raise AssertionError("connected client has no greeting")
            return self.greeting
        connection = socket.create_connection((self.host, self.port), timeout=self.timeout)
        connection.settimeout(self.timeout)
        self._socket = connection
        try:
            greeting = self._read_line()
            if greeting.startswith("ERR "):
                raise ServerError(greeting[4:])
            self.greeting = greeting
            return greeting
        except BaseException:
            self.close()
            raise

    def send(self, command: Command) -> str:
        """Send one validated command and return the server response."""

        connection = self._require_connection()
        try:
            connection.sendall((command.to_line() + "\n").encode("ascii"))
            response = self._read_line()
        except (OSError, UnicodeError) as error:
            self.close()
            raise ClientError(f"connection failed: {error}") from error
        if response.startswith("ERR "):
            raise ServerError(response[4:])
        return response

    def close(self) -> None:
        """Close the connection. Calling this method repeatedly is safe."""

        connection = self._socket
        self._socket = None
        self.greeting = None
        self._received.clear()
        if connection is not None:
            connection.close()

    def __enter__(self) -> TcpClient:
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _require_connection(self) -> socket.socket:
        if self._socket is None:
            raise ClientError("client is not connected")
        return self._socket

    def _read_line(self) -> str:
        connection = self._require_connection()
        while True:
            newline = self._received.find(b"\n")
            if newline >= 0:
                raw = bytes(self._received[:newline])
                del self._received[: newline + 1]
                return self._decode_line(raw)
            if len(self._received) > MAX_LINE_BYTES:
                raise ClientError("server line is too long")
            try:
                chunk = connection.recv(4096)
            except OSError as error:
                raise ClientError(f"connection failed: {error}") from error
            if not chunk:
                raise ClientError("server closed the connection")
            self._received.extend(chunk)

    @staticmethod
    def _decode_line(raw: bytes) -> str:
        if len(raw) > MAX_LINE_BYTES:
            raise ClientError("server line is too long")
        try:
            line = raw.decode("utf-8").rstrip("\r")
        except UnicodeDecodeError as error:
            raise ClientError("server sent invalid UTF-8") from error
        if not line:
            raise ClientError("server sent an empty line")
        return line


RomeoClient = TcpClient
