import main

def test_usa_il_nome_ricevuto_e_non_hardcode(monkeypatch):
    calls = []
    def resolve(name):
        calls.append(name)
        return "192.0.2.81"
    monkeypatch.setattr(main.socket, "gethostbyname", resolve)
    assert main.resolve_ipv4("robot.example") == "192.0.2.81"
    assert calls == ["robot.example"]
