def drive_then_stop(client, speed):
    """Invia FORWARD e garantisce STOP prima di chiudere."""
    with client.websocket_connect("/ws/control") as websocket:
        websocket.receive_json()
        forward_ack = None
        try:
            websocket.send_json({"command": "FORWARD", "speed": speed})
            forward_ack = websocket.receive_json()
        finally:
            websocket.send_json({"command": "STOP"})
            stop_ack = websocket.receive_json()
        return forward_ack, stop_ack
