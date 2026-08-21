import socket

client, server = socket.socketpair()
with client, server:
    client.sendall(b"PING\n")
    assert server.recv(16) == b"PING\n"
    server.sendall(b"PONG\n")
    assert client.recv(16) == b"PONG\n"
print("CLIENT SERVER OK")
