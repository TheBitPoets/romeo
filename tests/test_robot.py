import pytest

from romeo import Robot
from romeo.backends.factory import backend_override
from romeo.backends.mock import BackendCommand, MockBackend


def test_robot_drives_each_direction() -> None:
    backend = MockBackend()
    robot = Robot(backend)

    robot.forward(0.6)
    robot.backward(0.4)
    robot.left(0.3)
    robot.right(0.2)
    robot.stop()

    assert backend.history == [
        BackendCommand("set_motor_speeds", (0.6, 0.6)),
        BackendCommand("set_motor_speeds", (-0.4, -0.4)),
        BackendCommand("set_motor_speeds", (-0.3, 0.3)),
        BackendCommand("set_motor_speeds", (0.2, -0.2)),
        BackendCommand("stop", ()),
    ]


def test_speed_limit_is_applied() -> None:
    backend = MockBackend()
    robot = Robot(backend, speed_limit=0.35)

    robot.forward(0.8)

    assert (backend.left_speed, backend.right_speed) == (0.35, 0.35)


def test_independent_wheels_and_led_are_available_for_later_lessons() -> None:
    backend = MockBackend()
    robot = Robot(backend, speed_limit=0.6)

    robot.drive(-0.8, 0.25)
    robot.set_led(12, 34, 56)

    assert (backend.left_speed, backend.right_speed) == (-0.6, 0.25)
    assert backend.led_color == (12, 34, 56)


@pytest.mark.parametrize("color", [(-1, 0, 0), (0, 256, 0)])
def test_invalid_led_component_is_rejected(color: tuple[int, int, int]) -> None:
    with pytest.raises(ValueError, match="between 0 and 255"):
        Robot(MockBackend()).set_led(*color)


@pytest.mark.parametrize("speed", [-0.1, 1.1])
def test_invalid_speed_is_rejected(speed: float) -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        Robot(MockBackend()).forward(speed)


def test_context_manager_stops_and_closes_backend() -> None:
    backend = MockBackend()

    with Robot(backend) as robot:
        robot.forward()

    assert backend.closed
    assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)


def test_host_can_bind_backend_for_plain_robot_constructor() -> None:
    backend = MockBackend()

    with backend_override(backend):
        Robot().forward(0.2)

    assert (backend.left_speed, backend.right_speed) == (0.2, 0.2)
