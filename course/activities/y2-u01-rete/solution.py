from ipaddress import ip_address

def is_loopback(address):
    """Restituisce True se address indica questo stesso computer."""
    return ip_address(address).is_loopback
