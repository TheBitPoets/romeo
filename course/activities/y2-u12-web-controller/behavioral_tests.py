import pytest
from main import drive_then_stop

class Socket:
    def __init__(self, fail=False): self.sent=[]; self.count=0; self.fail=fail
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def send_json(self,data): self.sent.append(data)
    def receive_json(self):
        self.count += 1
        if self.fail and self.count == 2: raise RuntimeError("lost ack")
        return {"type":"ready"} if self.count==1 else {"type":"ack"}
class Client:
    def __init__(self,socket): self.socket=socket
    def websocket_connect(self,path): assert path=="/ws/control"; return self.socket

def test_velocita_variabile_e_stop():
    socket=Socket(); drive_then_stop(Client(socket), 0.37)
    assert socket.sent == [{"command":"FORWARD","speed":0.37},{"command":"STOP"}]

def test_stop_anche_se_ack_fallisce():
    socket=Socket(True)
    with pytest.raises(RuntimeError): drive_then_stop(Client(socket), 0.2)
    assert socket.sent[-1] == {"command":"STOP"}
