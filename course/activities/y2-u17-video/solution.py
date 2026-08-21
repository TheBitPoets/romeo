from romeo.camera.mock import MockCameraService

camera = MockCameraService()
frame = next(camera.frames(frames_per_second=10))
camera.close()
assert frame.startswith(b"\xff\xd8") and frame.endswith(b"\xff\xd9")
print("MJPEG FRAME OK")
