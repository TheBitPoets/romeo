from main import request_stop

class Socket:
    def __init__(self): self.received=iter([{"type":"ready"},{"type":"ack","command":"stop"}]); self.sent=[]; self.closed=False
    def __enter__(self): return self
    def __exit__(self,*args): self.closed=True
    def receive_json(self): return next(self.received)
    def send_json(self,data): self.sent.append(data)
class Client:
    def __init__(self): self.socket=Socket(); self.path=None
    def websocket_connect(self,path): self.path=path; return self.socket

def test_handshake_stop_ack_e_close():
    client=Client()
    assert request_stop(client)["command"] == "stop"
    assert client.path == "/ws/control"
    assert client.socket.sent == [{"command":"STOP"}] and client.socket.closed
