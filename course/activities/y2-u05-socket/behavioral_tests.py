import main

class Connection:
    def __init__(self):
        self.sent = []
        self.closed = False
    def __enter__(self): return self
    def __exit__(self, *args): self.closed = True
    def sendall(self, data): self.sent.append(data)
    def recv(self, size): return b"WELCOME\n"

def test_connette_invia_riceve_e_chiude(monkeypatch):
    connection = Connection()
    calls = []
    monkeypatch.setattr(main.socket, "create_connection", lambda endpoint, timeout: calls.append((endpoint, timeout)) or connection)
    assert main.tcp_request("127.0.0.1", 4321, b"CIAO\n") == b"WELCOME\n"
    assert calls == [(("127.0.0.1", 4321), 2.0)]
    assert connection.sent == [b"CIAO\n"] and connection.closed
