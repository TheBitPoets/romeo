from fastapi.testclient import TestClient
from main import create_status_app

def test_contratto_http_della_app():
    client=TestClient(create_status_app())
    assert client.get("/status").json() == {"robot":"romeo", "ready":True}
    assert client.post("/status").status_code == 405
