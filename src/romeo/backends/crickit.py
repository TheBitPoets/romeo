"""Adapter for the Adafruit CRICKIT HAT used by the physical Romeo robot."""

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CrickitConfig:
    """Physical wiring and calibration, overridable after hardware calibration."""

    left_motor_inverted: bool = False
    right_motor_inverted: bool = False
    left_trim: float = 0.0
    right_trim: float = 0.0
    max_speed: float = 1.0
    pan_min: float = 0.0
    pan_max: float = 180.0
    tilt_min: float = 0.0
    tilt_max: float = 180.0

    def __post_init__(self) -> None:
        for name in ("left_trim", "right_trim"):
            value = getattr(self, name)
            if isinstance(value, bool) or not math.isfinite(value) or not -1.0 <= value <= 1.0:
                raise ValueError(f"{name} must be finite and between -1 and 1")
        if (
            isinstance(self.max_speed, bool)
            or not math.isfinite(self.max_speed)
            or not 0.0 < self.max_speed <= 1.0
        ):
            raise ValueError("max_speed must be finite, greater than 0 and at most 1")
        for minimum, maximum, name in (
            (self.pan_min, self.pan_max, "pan"),
            (self.tilt_min, self.tilt_max, "tilt"),
        ):
            if not math.isfinite(minimum) or not math.isfinite(maximum):
                raise ValueError(f"{name} limits must be finite")
            if not 0.0 <= minimum < maximum <= 180.0:
                raise ValueError(f"{name} limits must satisfy 0 <= min < max <= 180")


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

    def configure(self, config: CrickitConfig) -> None:
        """Stop, then apply one validated physical-unit configuration."""

        self._ensure_open()
        self.stop()
        self.config = config

    def set_motor_speeds(self, left: float, right: float) -> None:
        self._ensure_open()
        left_value = self._trimmed(left, self.config.left_trim, self.config.max_speed)
        right_value = self._trimmed(right, self.config.right_trim, self.config.max_speed)
        left_value = -left_value if self.config.left_motor_inverted else left_value
        right_value = -right_value if self.config.right_motor_inverted else right_value
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

    def set_led_color(self, red: int, green: int, blue: int) -> None:
        self._ensure_open()
        packed_color = red << 16 | green << 8 | blue
        self._board.onboard_pixel.fill(packed_color)

    def stop(self) -> None:
        first_error: Exception | None = None
        for motor in (self._board.dc_motor_2, self._board.dc_motor_1):
            try:
                motor.throttle = 0.0
            except Exception as error:
                if first_error is None:
                    first_error = error
        if first_error is not None:
            raise first_error

    def close(self) -> None:
        if not self._closed:
            self.stop()
            self._closed = True

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("backend is closed")

    @staticmethod
    def _trimmed(value: float, trim: float, max_speed: float) -> float:
        """Apply proportional trim without exceeding the effective safety limit."""

        return max(-max_speed, min(max_speed, float(value) * (1.0 + trim)))
