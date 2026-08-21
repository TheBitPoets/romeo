from main import run_telepresence_session

class Response:
    def __init__(self,content=b"",data=None): self.status_code=200; self.content=content; self._data=data
    def json(self): return self._data
class Socket:
    def __init__(self): self.sent=[]; self.responses=iter([{"type":"ready"},{"type":"ack","n":1},{"type":"ack","n":2}])
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def send_json(self,data): self.sent.append(data)
    def receive_json(self): return next(self.responses)
class Client:
    def __init__(self): self.socket=Socket(); self.statuses=iter([{"moving":False,"n":1},{"moving":False,"n":2}])
    def get(self,path):
        return Response(b"jpeg-53") if path.endswith("photo") else Response(data=next(self.statuses))
    def websocket_connect(self,path): assert path=="/ws/control"; return self.socket

def test_integra_e_non_hardcode_dati_o_velocita():
    client=Client(); result=run_telepresence_session(client,0.43)
    assert result["photo"] == b"jpeg-53" and result["after"]["n"] == 2
    assert client.socket.sent == [{"command":"FORWARD","speed":0.43},{"command":"STOP"}]
