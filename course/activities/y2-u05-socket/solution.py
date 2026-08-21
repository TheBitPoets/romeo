import socket

def tcp_request(host, port, message=b"HELLO\n"):
    """Invia message a un server TCP e restituisce la risposta."""
    with socket.create_connection((host, port), timeout=2.0) as client:
        client.sendall(message)
        return client.recv(1024)
