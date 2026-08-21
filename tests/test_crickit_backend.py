from types import SimpleNamespace

import pytest

from romeo.backends.crickit import CrickitBackend, CrickitConfig


class FakePixel:
    def __init__(self) -> None:
        self.color = 0

    def fill(self, color: int) -> None:
        self.color = color


def fake_board() -> SimpleNamespace:
    return SimpleNamespace(
        dc_motor_1=SimpleNamespace(throttle=None),
        dc_motor_2=SimpleNamespace(throttle=None),
        servo_1=SimpleNamespace(angle=None),
        servo_4=SimpleNamespace(angle=None),
        onboard_pixel=FakePixel(),
    )


def test_crickit_wiring_and_calibration() -> None:
    board = fake_board()
    backend = CrickitBackend(
        board,
        CrickitConfig(left_motor_inverted=True, pan_min=30.0, pan_max=110.0),
    )

    backend.set_motor_speeds(0.4, -0.2)
    backend.set_camera_angles(10.0, 200.0)
    backend.set_led_color(10, 20, 30)

    assert board.dc_motor_2.throttle == -0.4
    assert board.dc_motor_1.throttle == -0.2
    assert board.servo_1.angle == 30.0
    assert board.servo_4.angle == 180.0
    assert board.onboard_pixel.color == 0x0A141E


def test_crickit_stops_after_motor_write_error() -> None:
    class BrokenMotor:
        @property
        def throttle(self) -> float:
            return 0.0

        @throttle.setter
        def throttle(self, value: float) -> None:
            if value != 0.0:
                raise OSError("I2C failure")

    board = fake_board()
    board.dc_motor_2 = BrokenMotor()
    backend = CrickitBackend(board)

    with pytest.raises(OSError, match="I2C failure"):
        backend.set_motor_speeds(0.5, 0.5)

    assert board.dc_motor_1.throttle == 0.0


def test_stop_attempts_both_motors_when_first_zero_write_fails() -> None:
    class BrokenStopMotor:
        @property
        def throttle(self) -> float:
            return 0.5

        @throttle.setter
        def throttle(self, value: float) -> None:
            raise OSError("left motor I2C failure")

    board = fake_board()
    board.dc_motor_2 = BrokenStopMotor()
    board.dc_motor_1.throttle = 0.5
    backend = CrickitBackend(board)

    with pytest.raises(OSError, match="left motor"):
        backend.stop()

    assert board.dc_motor_1.throttle == 0.0
