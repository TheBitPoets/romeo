"""Hardware-independent object-oriented API for Romeo."""

from types import TracebackType

from romeo.backends.base import Backend
from romeo.backends.factory import create_backend


class Robot:
    """Control Romeo with normalized speeds while hiding backend details."""

    def __init__(self, backend: Backend | None = None, *, speed_limit: float = 1.0) -> None:
        if not 0.0 < speed_limit <= 1.0:
            raise ValueError("speed_limit must be greater than 0 and at most 1")
        self._backend = backend or create_backend()
        self.speed_limit = speed_limit
        self._closed = False

    @property
    def backend(self) -> Backend:
        """Return the active backend for diagnostics and advanced use."""

        return self._backend

    def forward(self, speed: float = 0.5) -> None:
        value = self._speed(speed)
        self._drive(value, value)

    def backward(self, speed: float = 0.5) -> None:
        value = self._speed(speed)
        self._drive(-value, -value)

    def left(self, speed: float = 0.5) -> None:
        value = self._speed(speed)
        self._drive(-value, value)

    def right(self, speed: float = 0.5) -> None:
        value = self._speed(speed)
        self._drive(value, -value)

    def stop(self) -> None:
        self._backend.stop()

    def look(self, pan: float = 90.0, tilt: float = 90.0) -> None:
        if not 0.0 <= pan <= 180.0 or not 0.0 <= tilt <= 180.0:
            raise ValueError("pan and tilt must be between 0 and 180 degrees")
        self._ensure_open()
        self._backend.set_camera_angles(float(pan), float(tilt))

    def close(self) -> None:
        if not self._closed:
            self._backend.close()
            self._closed = True

    def __enter__(self) -> "Robot":
        self._ensure_open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _drive(self, left: float, right: float) -> None:
        self._ensure_open()
        self._backend.set_motor_speeds(left, right)

    def _speed(self, speed: float) -> float:
        if not 0.0 <= speed <= 1.0:
            raise ValueError("speed must be between 0 and 1")
        return min(float(speed), self.speed_limit)

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("robot is closed")

