from romeo.camera.mock import MINIMAL_JPEG, MockCameraService

camera = MockCameraService()
assert camera.available and camera.capture_photo() == MINIMAL_JPEG
camera.close()
print("CAMERA SERVICE OK")
