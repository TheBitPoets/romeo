import socket
from ipaddress import ip_address

def resolve_ipv4(hostname):
    """Risolve hostname e restituisce un indirizzo IPv4 valido."""
    address = socket.gethostbyname(hostname)
    if ip_address(address).version != 4:
        raise ValueError("il resolver non ha restituito IPv4")
    return address
