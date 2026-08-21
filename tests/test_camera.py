from __future__ import annotations

import threading
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor

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


def test_picamera2_serializes_concurrent_captures() -> None:
    class FakeCamera:
        def __init__(self) -> None:
            self.active = 0
            self.overlapped = False

        def create_video_configuration(self, **configuration: object) -> object:
            return configuration

        def configure(self, configuration: object) -> None:
            del configuration

        def start(self) -> None:
            return

        def capture_file(self, output: object, *, format: str) -> None:
            del format
            self.active += 1
            if self.active > 1:
                self.overlapped = True
            threading.Event().wait(0.02)
            output.write(b"jpeg")  # type: ignore[attr-defined]
            self.active -= 1

        def stop(self) -> None:
            return

        def close(self) -> None:
            return

    hardware = FakeCamera()
    camera = Picamera2CameraService(hardware, warmup_seconds=0)
    with ThreadPoolExecutor(max_workers=2) as executor:
        assert list(executor.map(lambda _: camera.capture_photo(), range(2))) == [
            b"jpeg",
            b"jpeg",
        ]
    assert not hardware.overlapped


def test_camera_close_still_closes_device_when_stop_fails() -> None:
    class BrokenStopCamera:
        def create_video_configuration(self, **configuration: object) -> object:
            return configuration

        def configure(self, configuration: object) -> None:
            del configuration

        def start(self) -> None:
            return

        def stop(self) -> None:
            raise RuntimeError("stop failed")

        def close(self) -> None:
            self.closed = True

    hardware = BrokenStopCamera()
    hardware.closed = False
    camera = Picamera2CameraService(hardware, warmup_seconds=0)
    camera.start()
    with pytest.raises(RuntimeError, match="stop failed"):
        camera.close()
    assert hardware.closed
    assert not camera.available


def test_mjpeg_chunks_have_explicit_boundaries_and_lengths() -> None:
    class OneFrameCamera(MockCameraService):
        def frames(self, *, frames_per_second: float = 10.0) -> Iterator[bytes]:
            del frames_per_second
            yield MINIMAL_JPEG

    chunk = next(_mjpeg_stream(OneFrameCamera()))

    assert chunk.startswith(b"--FRAME\r\nContent-Type: image/jpeg\r\n")
    assert b"Content-Length: 4\r\n\r\n" in chunk
    assert chunk.endswith(MINIMAL_JPEG + b"\r\n")


@pytest.mark.parametrize("warmup", [-1.0, float("nan"), float("inf")])
def test_camera_warmup_must_be_non_negative_and_finite(warmup: float) -> None:
    with pytest.raises(ValueError, match="non-negative finite"):
        Picamera2CameraService(object(), warmup_seconds=warmup)


@pytest.mark.hardware
@pytest.mark.skip(reason="requires a physical Raspberry Pi camera")
def test_physical_picamera2_capture() -> None:
    camera = Picamera2CameraService(warmup_seconds=0.2)
    try:
        assert camera.capture_photo().startswith(b"\xff\xd8")
    finally:
        camera.close()
