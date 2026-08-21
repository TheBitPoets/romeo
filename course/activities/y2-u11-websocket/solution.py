from fastapi.testclient import TestClient
from romeo.web import create_app

with TestClient(create_app()) as client:
    with client.websocket_connect("/ws/control") as websocket:
        ready = websocket.receive_json()
        websocket.send_json({"command": "STOP"})
        ack = websocket.receive_json()
        assert ready["type"] == "ready" and ack["type"] == "ack"
print("WEBSOCKET ACK OK")
