from main import choose_free_port

def test_restituisce_una_porta_effimera_valida():
    port = choose_free_port()
    assert isinstance(port, int)
    assert 0 < port < 65536
