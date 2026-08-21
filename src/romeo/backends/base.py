"""Small hardware-independent contract used by :class:`romeo.Robot`."""

from typing import Protocol


class Backend(Protocol):
    """Operations that every real, mock, or simulated Romeo backend provides."""

    def set_motor_speeds(self, left: float, right: float) -> None:
        """Set normalized wheel speeds in the inclusive range -1..1."""

    def set_camera_angles(self, pan: float, tilt: float) -> None:
        """Set camera pan and tilt angles in degrees."""

    def set_led_color(self, red: int, green: int, blue: int) -> None:
        """Set the onboard RGB LED using values in the inclusive range 0..255."""

    def stop(self) -> None:
        """Stop both motors immediately."""

    def close(self) -> None:
        """Release resources, leaving motors stopped."""
