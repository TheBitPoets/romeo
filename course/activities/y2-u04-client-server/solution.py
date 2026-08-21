def exchange_ping_pong(client, server):
    """Scambia PING e PONG sui due socket già collegati."""
    client.sendall(b"PING\n")
    request = server.recv(16)
    server.sendall(b"PONG\n")
    response = client.recv(16)
    return request, response
