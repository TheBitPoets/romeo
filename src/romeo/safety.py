"""Safety boundary shared by local, network, and physical robot control."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from contextlib import suppress

from romeo.backends.base import Backend


class ControllerBusyError(RuntimeError):
    """Raised when a second remote controller tries to take control."""


class ControllerAccessError(RuntimeError):
    """Raised when a command is sent without the active controller lease."""


class SafetyBackend:
    """Enforce speed, timeout, shutdown, and controller ownership rules."""

    def __init__(
        self,
        backend: Backend,
        *,
        max_speed: float = 0.7,
        command_timeout: float = 1.0,
        clock: Callable[[], float] = time.monotonic,
        background_watchdog: bool = True,
    ) -> None:
        if not 0.0 < max_speed <= 1.0:
            raise ValueError("max_speed must be greater than 0 and at most 1")
        if command_timeout <= 0.0:
            raise ValueError("command_timeout must be greater than 0")
        self.backend = backend
        self.max_speed = max_speed
        self.command_timeout = command_timeout
        self._clock = clock
        self._lock = threading.RLock()
        self._shutdown = threading.Event()
        self._deadline: float | None = None
        self._active_controller: str | None = None
        self._closed = False
        self._watchdog: threading.Thread | None = None
        if background_watchdog:
            self._watchdog = threading.Thread(
                target=self._watchdog_loop,
                name="romeo-safety-watchdog",
                daemon=True,
            )
            self._watchdog.start()

    @property
    def active_controller(self) -> str | None:
        with self._lock:
            return self._active_controller

    def claim_controller(self, controller_id: str) -> None:
        """Acquire the exclusive remote-control lease."""

        if not controller_id:
            raise ValueError("controller_id must not be empty")
        with self._lock:
            self._ensure_open()
            if self._active_controller not in (None, controller_id):
                raise ControllerBusyError("another controller is already active")
            self._active_controller = controller_id

    def release_controller(self, controller_id: str) -> None:
        """Release a lease and stop immediately, including on disconnect."""

        with self._lock:
            self._require_controller(controller_id)
            self._stop_locked()
            self._active_controller = None

    def set_motor_speeds(self, left: float, right: float) -> None:
        """Drive locally when no remote controller owns the robot."""

        with self._lock:
            if self._active_controller is not None:
                raise ControllerAccessError("robot is owned by a remote controller")
            self._set_motor_speeds_locked(left, right)

    def set_motor_speeds_for(self, controller_id: str, left: float, right: float) -> None:
        """Drive through an active remote-control lease."""

        with self._lock:
            self._require_controller(controller_id)
            self._set_motor_speeds_locked(left, right)

    def heartbeat(self, controller_id: str) -> None:
        """Keep a moving robot alive without changing wheel speed."""

        with self._lock:
            self._require_controller(controller_id)
            if self._deadline is not None:
                self._deadline = self._clock() + self.command_timeout

    def set_camera_angles(self, pan: float, tilt: float) -> None:
        with self._lock:
            self._ensure_open()
            self.backend.set_camera_angles(pan, tilt)

    def stop(self) -> None:
        with self._lock:
            self._stop_locked()

    def poll(self) -> bool:
        """Run one deterministic watchdog check; return whether it stopped Romeo."""

        with self._lock:
            if self._deadline is None or self._clock() < self._deadline:
                return False
            self._stop_locked()
            return True

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return
            self._stop_locked()
            self._closed = True
            self._shutdown.set()
        if self._watchdog is not None and self._watchdog is not threading.current_thread():
            self._watchdog.join(timeout=min(self.command_timeout, 1.0))
        self.backend.close()

    def _set_motor_speeds_locked(self, left: float, right: float) -> None:
        self._ensure_open()
        bounded_left = self._bounded_speed(left)
        bounded_right = self._bounded_speed(right)
        try:
            self.backend.set_motor_speeds(bounded_left, bounded_right)
        except Exception:
            self._best_effort_stop()
            raise
        self._deadline = (
            self._clock() + self.command_timeout
            if bounded_left != 0.0 or bounded_right != 0.0
            else None
        )

    def _stop_locked(self) -> None:
        self.backend.stop()
        self._deadline = None

    def _best_effort_stop(self) -> None:
        self._deadline = None
        with suppress(Exception):
            self.backend.stop()

    def _watchdog_loop(self) -> None:
        interval = min(0.1, self.command_timeout / 4.0)
        while not self._shutdown.wait(interval):
            try:
                self.poll()
            except Exception:
                self._best_effort_stop()

    def _bounded_speed(self, speed: float) -> float:
        if not -1.0 <= speed <= 1.0:
            raise ValueError("wheel speed must be between -1 and 1")
        return max(-self.max_speed, min(self.max_speed, float(speed)))

    def _require_controller(self, controller_id: str) -> None:
        self._ensure_open()
        if self._active_controller != controller_id:
            raise ControllerAccessError("controller does not own the robot")

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("safety backend is closed")
