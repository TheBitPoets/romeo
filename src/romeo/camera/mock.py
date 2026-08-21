"""Camera test doubles for CI and simulation hosts."""

import time
from collections.abc import Iterator

from romeo.camera.base import CameraUnavailableError

MINIMAL_JPEG = b"\xff\xd8\xff\xd9"


class MockCameraService:
    """Return deterministic JPEG bytes and record capture calls."""

    def __init__(self, frame: bytes = MINIMAL_JPEG) -> None:
        self.frame = frame
        self.capture_count = 0
        self.closed = False

    @property
    def available(self) -> bool:
        return not self.closed

    def capture_photo(self) -> bytes:
        if self.closed:
            raise CameraUnavailableError("camera is closed")
        self.capture_count += 1
        return self.frame

    def frames(self, *, frames_per_second: float = 10.0) -> Iterator[bytes]:
        if frames_per_second <= 0.0:
            raise ValueError("frames_per_second must be greater than zero")
        interval = 1.0 / frames_per_second
        while not self.closed:
            yield self.capture_photo()
            time.sleep(interval)

    def close(self) -> None:
        self.closed = True


class UnavailableCameraService:
    """Explicit null service used on hosts without a configured camera."""

    @property
    def available(self) -> bool:
        return False

    def capture_photo(self) -> bytes:
        raise CameraUnavailableError("camera is not configured")

    def frames(self, *, frames_per_second: float = 10.0) -> Iterator[bytes]:
        del frames_per_second
        raise CameraUnavailableError("camera is not configured")
        yield b""  # pragma: no cover - makes this a generator

    def close(self) -> None:
        return

