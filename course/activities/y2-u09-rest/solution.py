def read_robot_status(client):
    """Legge e valida la risorsa REST /api/status."""
    response = client.get("/api/status")
    if response.status_code != 200:
        raise ValueError("status REST inatteso")
    data = response.json()
    if "status" not in data or "moving" not in data:
        raise ValueError("risposta incompleta")
    return data
