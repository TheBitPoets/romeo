from fastapi.testclient import TestClient
from romeo.web import create_app

with TestClient(create_app()) as client:
    with client.websocket_connect("/ws/control") as control:
        control.receive_json()
        control.send_json({"command": "FORWARD", "speed": 0.2})
        assert control.receive_json()["type"] == "ack"
        control.send_json({"command": "STOP"})
        assert control.receive_json()["type"] == "ack"
    assert client.get("/api/status").json()["moving"] is False
print("INTEGRAZIONE OK")
