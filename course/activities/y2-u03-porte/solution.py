import socket

with socket.socket() as listener:
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    assert 0 < port < 65536
print("PORTA OK")
