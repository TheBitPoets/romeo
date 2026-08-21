"""Fail-safe, supervised active checks used while commissioning a Romeo unit."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from threading import Timer
from time import monotonic, sleep

from romeo.backends.base import Backend
from romeo.camera.base import CameraService
from romeo.safety import SafetyBackend

MAX_MOTOR_THROTTLE = 0.2
MAX_MOTOR_DURATION = 0.5

Input = Callable[[str], str]
Output = Callable[[str], None]
Wait = Callable[[float], None]


class MotorSide(str, Enum):
    """Motor selected for a supervised test."""

    LEFT = "left"
    RIGHT = "right"


class MotorObservation(str, Enum):
    """Observation reported by the supervising person."""

    FORWARD = "forward"
    REVERSED = "reversed"
    NO_MOVEMENT = "no_movement"


@dataclass(frozen=True, slots=True)
class MotorTestResult:
    """Result of one supervised single-motor test."""

    side: MotorSide
    observation: MotorObservation | None
    cancelled: bool = False

    @property
    def inversion_required(self) -> bool:
        """Whether the observed wheel direction requires polarity inversion."""

        return self.observation is MotorObservation.REVERSED


@dataclass(frozen=True, slots=True)
class ServoTestResult:
    pan: float
    tilt: float
    accepted: bool


@dataclass(frozen=True, slots=True)
class CameraTestResult:
    jpeg_bytes: int


@dataclass(frozen=True, slots=True)
class WatchdogMeasurement:
    samples_seconds: tuple[float, ...]

    @property
    def minimum_ms(self) -> float:
        return min(self.samples_seconds) * 1000.0

    @property
    def maximum_ms(self) -> float:
        return max(self.samples_seconds) * 1000.0

    @property
    def mean_ms(self) -> float:
        return sum(self.samples_seconds) * 1000.0 / len(self.samples_seconds)


class CommissionExecutor:
    """Run deliberately small active tests through the public backend contract.

    Input, output, and waiting are injectable so the interaction and every
    failure path can be tested without physical hardware.
    """

    def __init__(
        self,
        backend: Backend,
        *,
        input_fn: Input = input,
        output_fn: Output = print,
        wait_fn: Wait = sleep,
        clock_fn: Callable[[], float] = monotonic,
    ) -> None:
        self._backend = backend
        self._input = input_fn
        self._output = output_fn
        self._wait = wait_fn
        self._clock = clock_fn

    def test_motor(
        self,
        side: MotorSide | str,
        *,
        throttle: float = 0.15,
        duration: float = 0.4,
    ) -> MotorTestResult:
        """Test one motor after confirmation and ask its observed direction.

        Values beyond the commissioning safety envelope are rejected rather
        than clamped, so the person supervising the test sees configuration
        mistakes. The backend is stopped on every exit path, including
        cancellation, timeout, ``KeyboardInterrupt``, and other
        ``BaseException`` subclasses.
        """

        try:
            motor_side = self._validate(side, throttle, duration)
            self._describe_test(motor_side, throttle, duration)
            answer = self._input("[INVIO] continua, [q] annulla: ").strip().lower()
            if answer == "q":
                self._output("Test annullato. I motori restano fermi.")
                return MotorTestResult(side=motor_side, observation=None, cancelled=True)
            if answer:
                raise ValueError("premere INVIO per continuare oppure q per annullare")

            left = throttle if motor_side is MotorSide.LEFT else 0.0
            right = throttle if motor_side is MotorSide.RIGHT else 0.0
            self._backend.set_motor_speeds(left, right)
            emergency_timer = Timer(duration, self._backend.stop)
            emergency_timer.daemon = True
            emergency_timer.start()
            try:
                self._wait(duration)
            finally:
                emergency_timer.cancel()
                # Stop before waiting for a human observation; the wheel must
                # never remain powered while the supervisor reads or answers.
                self._backend.stop()

            observation = self._ask_observation()
            return MotorTestResult(side=motor_side, observation=observation)
        finally:
            self._backend.stop()

    def test_servo(
        self,
        pan: float,
        tilt: float,
        *,
        safe_pan: float | None = None,
        safe_tilt: float | None = None,
    ) -> ServoTestResult:
        """Move to one already validated conservative position after confirmation."""

        move_attempted = False
        try:
            if not 0.0 <= pan <= 180.0 or not 0.0 <= tilt <= 180.0:
                raise ValueError("servo angles must be between 0 and 180")
            answer = self._input(
                f"Posizione servo pan={pan:.1f}, tilt={tilt:.1f}. [INVIO] continua, [q] annulla: "
            ).strip().lower()
            if answer == "q":
                return ServoTestResult(pan=pan, tilt=tilt, accepted=False)
            if answer:
                raise ValueError("premere INVIO per continuare oppure q per annullare")
            move_attempted = True
            self._backend.set_camera_angles(pan, tilt)
            observed = self._input(
                "Movimento libero, senza buzzing o cavi in tensione? [s] sì, [n] no: "
            ).strip().lower()
            if observed not in {"s", "n"}:
                raise ValueError("risposta attesa: s oppure n")
            return ServoTestResult(pan=pan, tilt=tilt, accepted=observed == "s")
        finally:
            try:
                if move_attempted and safe_pan is not None and safe_tilt is not None:
                    self._backend.set_camera_angles(safe_pan, safe_tilt)
            finally:
                self._backend.stop()

    def measure_watchdog(
        self,
        *,
        repeats: int = 3,
        throttle: float = 0.1,
    ) -> WatchdogMeasurement:
        """Measure completed watchdog stops with the wheels safely lifted."""

        if not isinstance(self._backend, SafetyBackend):
            raise RuntimeError("watchdog measurement requires SafetyBackend")
        if not 1 <= repeats <= 10:
            raise ValueError("repeats must be between 1 and 10")
        if not 0.0 < throttle <= 0.1:
            raise ValueError("watchdog measurement throttle must be at most 0.1")
        answer = self._input(
            f"WATCHDOG: {repeats} prove a throttle {throttle:.2f}, ruote sollevate. "
            "[INVIO] continua, [q] annulla: "
        ).strip().lower()
        if answer == "q":
            raise RuntimeError("watchdog measurement cancelled")
        if answer:
            raise ValueError("premere INVIO per continuare oppure q per annullare")

        samples: list[float] = []
        for _ in range(repeats):
            previous = self._backend.last_watchdog_stop_at
            started = self._clock()
            fallback = Timer(self._backend.command_timeout + 0.25, self._backend.stop)
            fallback.daemon = True
            try:
                self._backend.set_motor_speeds(throttle, throttle)
                fallback.start()
                deadline = started + self._backend.command_timeout + 0.5
                while self._clock() <= deadline:
                    observed = self._backend.last_watchdog_stop_at
                    if observed is not None and observed != previous:
                        samples.append(observed - started)
                        break
                    sleep(min(0.01, self._backend.command_timeout / 10.0))
                else:
                    raise TimeoutError("watchdog did not confirm a motor stop")
            finally:
                fallback.cancel()
                self._backend.stop()
        result = WatchdogMeasurement(tuple(samples))
        self._output(
            "Watchdog misurato: "
            f"min {result.minimum_ms:.1f} ms, max {result.maximum_ms:.1f} ms, "
            f"media {result.mean_ms:.1f} ms."
        )
        return result

    def test_camera(self, camera: CameraService) -> CameraTestResult:
        """Capture one supervised JPEG while keeping motors stopped."""

        try:
            self._backend.stop()
            answer = self._input(
                "La camera acquisirà una foto di prova. [INVIO] continua, [q] annulla: "
            ).strip().lower()
            if answer == "q":
                raise RuntimeError("camera test cancelled")
            if answer:
                raise ValueError("premere INVIO per continuare oppure q per annullare")
            payload = camera.capture_photo()
            if not payload.startswith(b"\xff\xd8"):
                raise RuntimeError("camera did not return a JPEG image")
            return CameraTestResult(jpeg_bytes=len(payload))
        finally:
            self._backend.stop()
            camera.close()

    def _describe_test(self, side: MotorSide, throttle: float, duration: float) -> None:
        label = "SINISTRO" if side is MotorSide.LEFT else "DESTRO"
        self._output(f"TEST MOTORE {label}")
        self._output("Solleva Romeo: la ruota non deve toccare il pavimento.")
        self._output(
            f"Verrà applicato throttle {throttle:.2f} per {duration:.2f} secondi."
        )

    def _ask_observation(self) -> MotorObservation:
        answer = self._input(
            "La ruota ha girato nel verso AVANTI? [s] sì, [n] no, "
            "[x] non si è mossa: "
        ).strip().lower()
        observations = {
            "s": MotorObservation.FORWARD,
            "n": MotorObservation.REVERSED,
            "x": MotorObservation.NO_MOVEMENT,
        }
        try:
            return observations[answer]
        except KeyError as exc:
            raise ValueError("risposta attesa: s, n oppure x") from exc

    @staticmethod
    def _validate(side: MotorSide | str, throttle: float, duration: float) -> MotorSide:
        try:
            motor_side = MotorSide(side)
        except ValueError as exc:
            raise ValueError("side must be 'left' or 'right'") from exc
        if isinstance(throttle, bool) or not 0.0 < throttle <= MAX_MOTOR_THROTTLE:
            raise ValueError(f"throttle must be greater than 0 and at most {MAX_MOTOR_THROTTLE}")
        if isinstance(duration, bool) or not 0.0 < duration <= MAX_MOTOR_DURATION:
            raise ValueError(f"duration must be greater than 0 and at most {MAX_MOTOR_DURATION}")
        return motor_side
