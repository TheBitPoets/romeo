import socket
from ipaddress import ip_address

address = socket.gethostbyname("localhost")
assert ip_address(address).version == 4
print("IP OK", address)
