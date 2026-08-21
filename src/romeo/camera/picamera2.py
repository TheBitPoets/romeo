"""Modern Raspberry Pi camera adapter based on Picamera2/libcamera."""

from __future__ import annotations

import io
import math
import time
from collections.abc import Iterator
from typing import Any

from romeo.camera.base import CameraUnavailableError


class Picamera2CameraService:
    """Capture JPEG photos and frames with a lazily imported Picamera2 camera."""

    def __init__(
        self,
        camera: Any | None = None,
        *,
        resolution: tuple[int, int] = (640, 480),
        warmup_seconds: float = 1.0,
    ) -> None:
        if resolution[0] <= 0 or resolution[1] <= 0:
            raise ValueError("resolution dimensions must be positive")
        if warmup_seconds < 0.0:
            raise ValueError("warmup_seconds must not be negative")
        if camera is None:
            try:
                from picamera2 import Picamera2  # type: ignore[import-not-found]
            except ImportError as error:
                raise CameraUnavailableError(
                    "Picamera2 is not installed; install it from Raspberry Pi OS packages"
                ) from error
            camera = Picamera2()
        self._camera: Any = camera
        self.resolution = resolution
        self.warmup_seconds = warmup_seconds
        self._started = False
        self._closed = False

    @property
    def available(self) -> bool:
        return not self._closed

    def start(self) -> None:
        if self._closed:
            raise CameraUnavailableError("camera is closed")
        if self._started:
            return
        configuration = self._camera.create_video_configuration(
            main={"size": self.resolution}
        )
        self._camera.configure(configuration)
        self._camera.start()
        if self.warmup_seconds:
            time.sleep(self.warmup_seconds)
        self._started = True

    def capture_photo(self) -> bytes:
        self.start()
        output = io.BytesIO()
        self._camera.capture_file(output, format="jpeg")
        return output.getvalue()

    def frames(self, *, frames_per_second: float = 10.0) -> Iterator[bytes]:
        if not math.isfinite(frames_per_second) or frames_per_second <= 0.0:
            raise ValueError("frames_per_second must be a positive finite number")
        interval = 1.0 / frames_per_second
        while not self._closed:
            started_at = time.monotonic()
            yield self.capture_photo()
            remaining = interval - (time.monotonic() - started_at)
            if remaining > 0.0:
                time.sleep(remaining)

    def close(self) -> None:
        if self._closed:
            return
        if self._started:
            self._camera.stop()
        self._camera.close()
        self._closed = True
        self._started = False

