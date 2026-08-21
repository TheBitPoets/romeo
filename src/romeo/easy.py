"""Function-based API for students taking their first steps in Python."""

from romeo.backends.base import Backend
from romeo.robot import Robot

_robot: Robot | None = None


def forward(speed: float = 0.5) -> None:
    _current_robot().forward(speed)


def backward(speed: float = 0.5) -> None:
    _current_robot().backward(speed)


def left(speed: float = 0.5) -> None:
    _current_robot().left(speed)


def right(speed: float = 0.5) -> None:
    _current_robot().right(speed)


def stop() -> None:
    _current_robot().stop()


def look(pan: float = 90.0, tilt: float = 90.0) -> None:
    _current_robot().look(pan, tilt)


def use_backend(backend: Backend, *, speed_limit: float = 1.0) -> None:
    """Select a backend before issuing commands, primarily for hosts and tests."""

    global _robot
    if _robot is not None:
        _robot.close()
    _robot = Robot(backend, speed_limit=speed_limit)


def close() -> None:
    """Stop Romeo and release backend resources."""

    global _robot
    if _robot is not None:
        _robot.close()
        _robot = None


def _current_robot() -> Robot:
    global _robot
    if _robot is None:
        _robot = Robot()
    return _robot

