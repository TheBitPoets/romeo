from __future__ import annotations

from collections.abc import Iterator

import pytest

from romeo.camera.base import CameraUnavailableError
from romeo.camera.mock import MINIMAL_JPEG, MockCameraService, UnavailableCameraService
from romeo.camera.picamera2 import Picamera2CameraService
from romeo.web.app import _mjpeg_stream


def test_mock_camera_is_deterministic_and_closable() -> None:
    camera = MockCameraService(b"jpeg-data")

    assert camera.capture_photo() == b"jpeg-data"
    assert camera.capture_count == 1
    camera.close()

    with pytest.raises(CameraUnavailableError, match="closed"):
        camera.capture_photo()


def test_unavailable_camera_reports_capability() -> None:
    camera = UnavailableCameraService()

    assert not camera.available
    with pytest.raises(CameraUnavailableError, match="not configured"):
        camera.capture_photo()


def test_picamera2_adapter_uses_current_capture_file_flow() -> None:
    output_bytes = b"\xff\xd8picture\xff\xd9"

    class FakeCamera:
        def __init__(self) -> None:
            self.calls: list[object] = []

        def create_video_configuration(self, **configuration: object) -> object:
            self.calls.append(("create_video_configuration", configuration))
            return {"configuration": configuration}

        def configure(self, configuration: object) -> None:
            self.calls.append(("configure", configuration))

        def start(self) -> None:
            self.calls.append("start")

        def capture_file(self, output: object, *, format: str) -> None:
            self.calls.append(("capture_file", format))
            output.write(output_bytes)  # type: ignore[attr-defined]

        def stop(self) -> None:
            self.calls.append("stop")

        def close(self) -> None:
            self.calls.append("close")

    hardware = FakeCamera()
    camera = Picamera2CameraService(hardware, resolution=(320, 240), warmup_seconds=0.0)

    assert camera.capture_photo() == output_bytes
    camera.close()

    assert hardware.calls[0] == (
        "create_video_configuration",
        {"main": {"size": (320, 240)}},
    )
    assert hardware.calls[-2:] == ["stop", "close"]


def test_mjpeg_chunks_have_explicit_boundaries_and_lengths() -> None:
    class OneFrameCamera(MockCameraService):
        def frames(self, *, frames_per_second: float = 10.0) -> Iterator[bytes]:
            del frames_per_second
            yield MINIMAL_JPEG

    chunk = next(_mjpeg_stream(OneFrameCamera()))

    assert chunk.startswith(b"--FRAME\r\nContent-Type: image/jpeg\r\n")
    assert b"Content-Length: 4\r\n\r\n" in chunk
    assert chunk.endswith(MINIMAL_JPEG + b"\r\n")


@pytest.mark.hardware
@pytest.mark.skip(reason="requires a physical Raspberry Pi camera")
def test_physical_picamera2_capture() -> None:
    camera = Picamera2CameraService(warmup_seconds=0.2)
    try:
        assert camera.capture_photo().startswith(b"\xff\xd8")
    finally:
        camera.close()
