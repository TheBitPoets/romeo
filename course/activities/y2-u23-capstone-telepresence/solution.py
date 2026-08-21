from fastapi.testclient import TestClient
from romeo.camera.mock import MockCameraService
from romeo.web import create_app

with TestClient(create_app(camera=MockCameraService())) as client:
    assert client.get("/api/camera/photo").status_code == 200
    assert client.get("/api/status").json()["status"] == "ok"
    with client.websocket_connect("/ws/control") as control:
        control.receive_json()
        control.send_json({"command": "FORWARD", "speed": 0.2})
        assert control.receive_json()["command"] == "forward"
        control.send_json({"command": "STOP"})
        assert control.receive_json()["command"] == "stop"
    assert client.get("/api/status").json()["moving"] is False
print("FOTO OK")
print("CONTROLLO WS OK")
print("TELEMETRIA STOP OK")
