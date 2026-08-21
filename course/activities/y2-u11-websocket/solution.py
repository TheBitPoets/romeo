def request_stop(client):
    """Apre /ws/control, invia STOP e restituisce l'ack."""
    with client.websocket_connect("/ws/control") as websocket:
        ready = websocket.receive_json()
        if ready.get("type") != "ready":
            raise ValueError("WebSocket non pronto")
        websocket.send_json({"command": "STOP"})
        ack = websocket.receive_json()
        if ack.get("type") != "ack":
            raise ValueError("ack mancante")
        return ack
