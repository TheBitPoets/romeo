from fastapi.testclient import TestClient
from romeo.web import create_app

with TestClient(create_app()) as client:
    response = client.get("/api/status")
    data = response.json()
    assert response.status_code == 200 and data["status"] == "ok"
print("REST STATUS OK")
