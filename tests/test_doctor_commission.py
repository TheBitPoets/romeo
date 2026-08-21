from __future__ import annotations

import threading
from collections.abc import Iterator

import pytest

from romeo.backends.mock import BackendCommand, MockBackend
from romeo.camera.mock import MockCameraService
from romeo.doctor.commission import (
    CommissionExecutor,
    MotorObservation,
    MotorSide,
)
from romeo.safety import SafetyBackend


def answers(*values: str) -> Iterator[str]:
    return iter(values)


def test_left_motor_is_run_alone_and_stopped() -> None:
    backend = MockBackend()
    prompts = answers("", "s")
    waits: list[float] = []
    executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: next(prompts),
        output_fn=lambda _message: None,
        wait_fn=waits.append,
    )

    result = executor.test_motor(MotorSide.LEFT, throttle=0.15, duration=0.4)

    assert result.observation is MotorObservation.FORWARD
    assert result.inversion_required is False
    assert waits == [0.4]
    assert backend.history == [
        BackendCommand("set_motor_speeds", (0.15, 0.0)),
        BackendCommand("stop", ()),
        BackendCommand("stop", ()),
    ]


def test_right_motor_records_observed_reversed_polarity() -> None:
    backend = MockBackend()
    prompts = answers("", "n")
    executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: next(prompts),
        output_fn=lambda _message: None,
        wait_fn=lambda _duration: None,
    )

    result = executor.test_motor("right")

    assert result.observation is MotorObservation.REVERSED
    assert result.inversion_required is True
    assert backend.history[0] == BackendCommand("set_motor_speeds", (0.0, 0.15))
    assert backend.history[-1] == BackendCommand("stop", ())


def test_motor_is_stopped_before_requesting_the_observation() -> None:
    backend = MockBackend()
    prompts = answers("", "s")

    def read(_prompt: str) -> str:
        answer = next(prompts)
        if answer == "s":
            assert backend.left_speed == 0.0
            assert backend.right_speed == 0.0
        return answer

    CommissionExecutor(
        backend,
        input_fn=read,
        output_fn=lambda _message: None,
        wait_fn=lambda _duration: None,
    ).test_motor("left")


def test_cancel_stops_without_moving() -> None:
    backend = MockBackend()
    executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: "q",
        output_fn=lambda _message: None,
        wait_fn=lambda _duration: pytest.fail("cancelled test must not wait"),
    )

    result = executor.test_motor("left")

    assert result.cancelled is True
    assert result.observation is None
    assert backend.history == [BackendCommand("stop", ())]


@pytest.mark.parametrize(
    "failure",
    [RuntimeError("failure"), KeyboardInterrupt(), TimeoutError("timeout")],
    ids=["exception", "keyboard-interrupt", "timeout"],
)
def test_wait_failure_always_stops(failure: BaseException) -> None:
    backend = MockBackend()

    def fail_wait(_duration: float) -> None:
        raise failure

    executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: "",
        output_fn=lambda _message: None,
        wait_fn=fail_wait,
    )

    with pytest.raises(type(failure)):
        executor.test_motor("left")

    assert backend.left_speed == 0.0
    assert backend.right_speed == 0.0
    assert backend.history[-1] == BackendCommand("stop", ())


class EmergencyStop(BaseException):
    pass


def test_arbitrary_base_exception_always_stops() -> None:
    backend = MockBackend()

    def abort(_duration: float) -> None:
        raise EmergencyStop

    executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: "",
        output_fn=lambda _message: None,
        wait_fn=abort,
    )

    with pytest.raises(EmergencyStop):
        executor.test_motor("right")

    assert backend.history[-1] == BackendCommand("stop", ())


@pytest.mark.parametrize(
    ("throttle", "duration"),
    [(0.201, 0.4), (0.15, 0.501), (0.0, 0.4), (0.15, 0.0)],
)
def test_safety_limits_are_hard_and_invalid_test_still_stops(
    throttle: float, duration: float
) -> None:
    backend = MockBackend()
    executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: pytest.fail("invalid test must not prompt"),
        output_fn=lambda _message: None,
    )

    with pytest.raises(ValueError):
        executor.test_motor("left", throttle=throttle, duration=duration)

    assert backend.history == [BackendCommand("stop", ())]


def test_output_and_prompts_are_injectable() -> None:
    backend = MockBackend()
    prompts = answers("", "x")
    prompt_text: list[str] = []
    messages: list[str] = []

    def read(prompt: str) -> str:
        prompt_text.append(prompt)
        return next(prompts)

    result = CommissionExecutor(
        backend,
        input_fn=read,
        output_fn=messages.append,
        wait_fn=lambda _duration: None,
    ).test_motor("left")

    assert result.observation is MotorObservation.NO_MOVEMENT
    assert len(prompt_text) == 2
    assert messages[0] == "TEST MOTORE SINISTRO"
    assert any("Solleva Romeo" in message for message in messages)


def test_independent_timer_stops_motor_even_if_wait_blocks() -> None:
    backend = MockBackend()
    prompts = answers("", "s")

    def blocking_wait(_duration: float) -> None:
        threading.Event().wait(0.04)
        assert backend.left_speed == 0.0

    CommissionExecutor(
        backend,
        input_fn=lambda _prompt: next(prompts),
        output_fn=lambda _message: None,
        wait_fn=blocking_wait,
    ).test_motor("left", throttle=0.1, duration=0.01)


def test_servo_error_and_camera_error_leave_motors_stopped() -> None:
    backend = MockBackend()
    backend.set_motor_speeds(0.1, 0.1)
    servo_executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: (_ for _ in ()).throw(KeyboardInterrupt()),
        output_fn=lambda _message: None,
    )
    with pytest.raises(KeyboardInterrupt):
        servo_executor.test_servo(90, 90)
    assert backend.left_speed == backend.right_speed == 0.0

    camera = MockCameraService(b"not-jpeg")
    camera_executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: "",
        output_fn=lambda _message: None,
    )
    with pytest.raises(RuntimeError, match="JPEG"):
        camera_executor.test_camera(camera)
    assert backend.left_speed == backend.right_speed == 0.0
    assert not camera.available


def test_rejected_servo_position_returns_to_safe_center() -> None:
    backend = MockBackend()
    prompts = answers("", "n")

    result = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: next(prompts),
        output_fn=lambda _message: None,
    ).test_servo(45, 60, safe_pan=90, safe_tilt=90)

    assert not result.accepted
    assert backend.pan_angle == 90
    assert backend.tilt_angle == 90
    assert backend.left_speed == backend.right_speed == 0.0


def test_servo_recenter_failure_is_not_hidden_and_still_stops() -> None:
    class RecenterFailureBackend(MockBackend):
        calls = 0

        def set_camera_angles(self, pan: float, tilt: float) -> None:
            self.calls += 1
            if self.calls == 2:
                raise OSError("recenter failed")
            super().set_camera_angles(pan, tilt)

    backend = RecenterFailureBackend()
    prompts = answers("", "s")

    with pytest.raises(OSError, match="recenter failed"):
        CommissionExecutor(
            backend,
            input_fn=lambda _prompt: next(prompts),
            output_fn=lambda _message: None,
        ).test_servo(45, 60, safe_pan=90, safe_tilt=90)

    assert backend.left_speed == backend.right_speed == 0.0


def test_watchdog_is_measured_repeatedly_and_stops() -> None:
    raw_backend = MockBackend()
    backend = SafetyBackend(raw_backend, command_timeout=0.05)
    executor = CommissionExecutor(
        backend,
        input_fn=lambda _prompt: "",
        output_fn=lambda _message: None,
    )

    measurement = executor.measure_watchdog(repeats=3)

    assert len(measurement.samples_seconds) == 3
    assert 50 <= measurement.minimum_ms < 300
    assert measurement.minimum_ms <= measurement.mean_ms <= measurement.maximum_ms
    assert raw_backend.left_speed == raw_backend.right_speed == 0.0
    backend.close()


def test_watchdog_measurement_requires_safety_backend() -> None:
    executor = CommissionExecutor(
        MockBackend(), input_fn=lambda _prompt: "", output_fn=lambda _message: None
    )

    with pytest.raises(RuntimeError, match="SafetyBackend"):
        executor.measure_watchdog()
