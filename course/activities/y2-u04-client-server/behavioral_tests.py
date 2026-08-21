from main import exchange_ping_pong

class Endpoint:
    def __init__(self, incoming):
        self.incoming = incoming
        self.sent = []
    def sendall(self, data):
        self.sent.append(data)
    def recv(self, size):
        assert size > 0
        return self.incoming

def test_scambia_byte_nei_due_sensi():
    client = Endpoint(b"PONG\n")
    server = Endpoint(b"PING\n")
    assert exchange_ping_pong(client, server) == (b"PING\n", b"PONG\n")
    assert client.sent == [b"PING\n"]
    assert server.sent == [b"PONG\n"]
