from ipaddress import ip_address

loopback = ip_address("127.0.0.1")
assert loopback.is_loopback
print("RETE OK")
