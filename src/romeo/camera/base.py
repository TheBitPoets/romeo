"""Camera contract independent of Picamera2 and web transports."""

from collections.abc import Iterator
from typing import Protocol


class CameraUnavailableError(RuntimeError):
    """Raised when an operation needs a camera that is not available."""


class CameraService(Protocol):
    @property
    def available(self) -> bool:
        """Whether capture can currently be attempted."""

    def capture_photo(self) -> bytes:
        """Capture one JPEG image."""

    def frames(self, *, frames_per_second: float = 10.0) -> Iterator[bytes]:
        """Yield JPEG frames for a simple MJPEG stream."""

    def close(self) -> None:
        """Release the camera safely."""

