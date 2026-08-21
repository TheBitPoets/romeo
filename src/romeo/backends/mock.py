"""Explicit test double for backend calls; it does not simulate motion."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BackendCommand:
    """One command recorded by :class:`MockBackend`."""

    name: str
    values: tuple[float, ...]


class MockBackend:
    """In-memory backend with inspectable state and command history."""

    def __init__(self) -> None:
        self.left_speed = 0.0
        self.right_speed = 0.0
        self.pan_angle = 90.0
        self.tilt_angle = 90.0
        self.led_color = (0, 0, 0)
        self.closed = False
        self.history: list[BackendCommand] = []

    def set_motor_speeds(self, left: float, right: float) -> None:
        self._ensure_open()
        self.left_speed = left
        self.right_speed = right
        self.history.append(BackendCommand("set_motor_speeds", (left, right)))

    def set_camera_angles(self, pan: float, tilt: float) -> None:
        self._ensure_open()
        self.pan_angle = pan
        self.tilt_angle = tilt
        self.history.append(BackendCommand("set_camera_angles", (pan, tilt)))

    def set_led_color(self, red: int, green: int, blue: int) -> None:
        self._ensure_open()
        self.led_color = (red, green, blue)
        self.history.append(BackendCommand("set_led_color", (red, green, blue)))

    def stop(self) -> None:
        self.left_speed = 0.0
        self.right_speed = 0.0
        self.history.append(BackendCommand("stop", ()))

    def close(self) -> None:
        if not self.closed:
            self.stop()
            self.closed = True
            self.history.append(BackendCommand("close", ()))

    def _ensure_open(self) -> None:
        if self.closed:
            raise RuntimeError("backend is closed")
