"""Adapter for the Adafruit CRICKIT HAT used by the physical Romeo robot."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CrickitConfig:
    """Physical wiring and calibration, overridable after hardware calibration."""

    left_motor_inverted: bool = False
    right_motor_inverted: bool = False
    pan_min: float = 0.0
    pan_max: float = 180.0
    tilt_min: float = 0.0
    tilt_max: float = 180.0


class CrickitBackend:
    """Drive motor 2 (left), motor 1 (right), servo 1 (pan), and servo 4 (tilt)."""

    def __init__(self, board: Any | None = None, config: CrickitConfig | None = None) -> None:
        if board is None:
            try:
                from adafruit_crickit import (  # type: ignore[import-not-found]
                    crickit as loaded_board,
                )
            except ImportError as exc:
                raise RuntimeError(
                    "CRICKIT support is not installed; install the 'hardware' extra"
                ) from exc
            board = loaded_board
        self._board: Any = board
        self.config = config or CrickitConfig()
        self._closed = False

    def set_motor_speeds(self, left: float, right: float) -> None:
        self._ensure_open()
        left_value = -left if self.config.left_motor_inverted else left
        right_value = -right if self.config.right_motor_inverted else right
        try:
            self._board.dc_motor_2.throttle = left_value
            self._board.dc_motor_1.throttle = right_value
        except Exception:
            self.stop()
            raise

    def set_camera_angles(self, pan: float, tilt: float) -> None:
        self._ensure_open()
        bounded_pan = min(self.config.pan_max, max(self.config.pan_min, pan))
        bounded_tilt = min(self.config.tilt_max, max(self.config.tilt_min, tilt))
        self._board.servo_1.angle = bounded_pan
        self._board.servo_4.angle = bounded_tilt

    def stop(self) -> None:
        self._board.dc_motor_2.throttle = 0.0
        self._board.dc_motor_1.throttle = 0.0

    def close(self) -> None:
        if not self._closed:
            self.stop()
            self._closed = True

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("backend is closed")
