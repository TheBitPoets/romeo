import socket
import threading

listener = socket.socket()
listener.bind(("127.0.0.1", 0))
listener.listen(1)
port = listener.getsockname()[1]

def serve():
    connection, _ = listener.accept()
    with connection:
        assert connection.recv(16) == b"HELLO\n"
        connection.sendall(b"WELCOME\n")

thread = threading.Thread(target=serve)
thread.start()
with socket.create_connection(("127.0.0.1", port)) as client:
    client.sendall(b"HELLO\n")
    assert client.recv(16) == b"WELCOME\n"
thread.join()
listener.close()
print("SOCKET OK")
