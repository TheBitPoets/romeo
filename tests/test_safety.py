import threading

import pytest

from romeo.backends.mock import BackendCommand, MockBackend
from romeo.safety import ControllerAccessError, ControllerBusyError, SafetyBackend


class FakeClock:
    def __init__(self) -> None:
        self.now = 10.0

    def __call__(self) -> float:
        return self.now


def safe_backend(
    backend: MockBackend | None = None,
    *,
    clock: FakeClock | None = None,
) -> tuple[SafetyBackend, MockBackend, FakeClock]:
    inner = backend or MockBackend()
    fake_clock = clock or FakeClock()
    safety = SafetyBackend(
        inner,
        max_speed=0.6,
        command_timeout=0.5,
        clock=fake_clock,
        background_watchdog=False,
    )
    return safety, inner, fake_clock


def test_speed_is_limited_before_reaching_hardware() -> None:
    safety, backend, _ = safe_backend()

    safety.set_motor_speeds(1.0, -0.9)

    assert (backend.left_speed, backend.right_speed) == (0.6, -0.6)


def test_watchdog_stops_after_command_timeout() -> None:
    safety, backend, clock = safe_backend()
    safety.set_motor_speeds(0.5, 0.5)

    clock.now += 0.49
    assert not safety.poll()
    clock.now += 0.02
    assert safety.poll()
    assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)


def test_heartbeat_extends_watchdog_deadline() -> None:
    safety, backend, clock = safe_backend()
    safety.claim_controller("browser-1")
    safety.set_motor_speeds_for("browser-1", 0.5, 0.5)

    clock.now += 0.4
    safety.heartbeat("browser-1")
    clock.now += 0.4

    assert not safety.poll()
    assert backend.left_speed == 0.5


def test_only_one_controller_can_drive_and_disconnect_stops() -> None:
    safety, backend, _ = safe_backend()
    safety.claim_controller("keyboard")

    with pytest.raises(ControllerBusyError):
        safety.claim_controller("gamepad")
    with pytest.raises(ControllerAccessError):
        safety.set_motor_speeds(0.3, 0.3)
    with pytest.raises(ControllerAccessError):
        safety.set_camera_angles(20.0, 30.0)

    safety.set_motor_speeds_for("keyboard", 0.3, 0.3)
    safety.set_camera_angles_for("keyboard", 20.0, 30.0)
    safety.release_controller("keyboard")

    assert safety.active_controller is None
    assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)
    assert (backend.pan_angle, backend.tilt_angle) == (20.0, 30.0)


def test_close_is_idempotent_and_leaves_motors_zero() -> None:
    safety, backend, _ = safe_backend()
    safety.set_motor_speeds(0.5, 0.5)

    safety.close()
    safety.close()

    assert backend.closed
    assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)
    assert backend.history[-2:] == [BackendCommand("stop", ()), BackendCommand("close", ())]


def test_backend_failure_triggers_emergency_stop() -> None:
    class FailingBackend(MockBackend):
        def set_motor_speeds(self, left: float, right: float) -> None:
            self.left_speed = left
            self.right_speed = right
            raise OSError("motor controller unavailable")

    backend = FailingBackend()
    safety, _, _ = safe_backend(backend)

    with pytest.raises(OSError, match="unavailable"):
        safety.set_motor_speeds(0.4, 0.4)

    assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)


def test_background_watchdog_stops_without_manual_poll() -> None:
    stopped = threading.Event()

    class ObservableBackend(MockBackend):
        def stop(self) -> None:
            super().stop()
            stopped.set()

    backend = ObservableBackend()
    safety = SafetyBackend(backend, command_timeout=0.03, background_watchdog=True)
    safety.set_motor_speeds(0.4, 0.4)

    assert stopped.wait(timeout=1.0)
    assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)
    safety.close()


@pytest.mark.parametrize("timeout", [0.0, -1.0, float("nan"), float("inf")])
def test_command_timeout_must_be_positive_and_finite(timeout: float) -> None:
    with pytest.raises(ValueError, match="positive finite"):
        SafetyBackend(MockBackend(), command_timeout=timeout)
