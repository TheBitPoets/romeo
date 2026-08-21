import pytest
from main import read_robot_status

class Response:
    status_code=200
    def json(self): return {"status":"ok", "moving":True, "nonce":17}
class Client:
    def __init__(self): self.paths=[]
    def get(self, path): self.paths.append(path); return Response()

def test_legge_la_risorsa_senza_hardcode():
    client=Client()
    assert read_robot_status(client)["nonce"] == 17
    assert client.paths == ["/api/status"]
