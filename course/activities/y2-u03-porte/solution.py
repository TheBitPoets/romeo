import socket

def choose_free_port():
    """Chiede al sistema una porta libera sul loopback."""
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]
