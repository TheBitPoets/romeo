def control_and_read(client, speed):
    """Muove via WebSocket, garantisce STOP e legge lo stato REST."""
    with client.websocket_connect("/ws/control") as control:
        control.receive_json()
        try:
            control.send_json({"command":"FORWARD", "speed":speed})
            control.receive_json()
        finally:
            control.send_json({"command":"STOP"})
            control.receive_json()
    state = client.get("/api/status").json()
    if state.get("moving") is not False:
        raise ValueError("Romeo non è fermo")
    return state
