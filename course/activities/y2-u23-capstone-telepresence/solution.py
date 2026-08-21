def run_telepresence_session(client, speed=0.2):
    """Integra foto, stato, controllo realtime e STOP fail-safe."""
    photo_response = client.get("/api/camera/photo")
    if photo_response.status_code != 200:
        raise ValueError("foto non disponibile")
    before = client.get("/api/status").json()
    with client.websocket_connect("/ws/control") as control:
        control.receive_json()
        try:
            control.send_json({"command":"FORWARD", "speed":speed})
            forward_ack = control.receive_json()
        finally:
            control.send_json({"command":"STOP"})
            stop_ack = control.receive_json()
    after = client.get("/api/status").json()
    if after.get("moving") is not False:
        raise ValueError("STOP non confermato")
    return {"photo":photo_response.content, "before":before, "after":after, "acks":[forward_ack,stop_ack]}
