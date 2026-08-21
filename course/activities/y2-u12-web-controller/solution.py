from fastapi.testclient import TestClient
from romeo.web import create_app

with TestClient(create_app()) as client:
    with client.websocket_connect("/ws/control") as websocket:
        websocket.receive_json()
        websocket.send_json({"command": "FORWARD", "speed": 0.25})
        assert websocket.receive_json()["command"] == "forward"
        websocket.send_json({"command": "STOP"})
        assert websocket.receive_json()["command"] == "stop"
print("WEB CONTROL OK")
