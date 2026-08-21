from main import control_and_read

class Socket:
    def __init__(self): self.sent=[]; self.responses=iter([{"type":"ready"},{"type":"ack"},{"type":"ack"}])
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def send_json(self,data): self.sent.append(data)
    def receive_json(self): return next(self.responses)
class Response:
    def json(self): return {"moving":False,"nonce":29}
class Client:
    def __init__(self): self.socket=Socket(); self.paths=[]
    def websocket_connect(self,path): assert path=="/ws/control"; return self.socket
    def get(self,path): self.paths.append(path); return Response()

def test_controllo_stop_e_stato_non_hardcoded():
    client=Client(); state=control_and_read(client,0.41)
    assert client.socket.sent == [{"command":"FORWARD","speed":0.41},{"command":"STOP"}]
    assert client.paths == ["/api/status"] and state["nonce"] == 29
