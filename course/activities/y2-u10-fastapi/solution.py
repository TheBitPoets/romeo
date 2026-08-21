from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/status")
def status():
    return {"robot": "romeo", "ready": True}

response = TestClient(app).get("/status")
assert response.status_code == 200 and response.json()["ready"] is True
print("FASTAPI OK")
