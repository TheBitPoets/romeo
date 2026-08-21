from fastapi.testclient import TestClient
from romeo.camera.mock import MINIMAL_JPEG, MockCameraService
from romeo.web import create_app

with TestClient(create_app(camera=MockCameraService())) as client:
    response = client.get("/api/camera/photo")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert response.content == MINIMAL_JPEG
print("FOTO JPEG OK")
