from main import commands_for_keys

def test_mappa_tasti_e_stop_finale():
    assert commands_for_keys(["W", "x", "a"]) == ["FORWARD", "LEFT", "STOP"]
    assert commands_for_keys([]) == ["STOP"]
    assert commands_for_keys([" "]) == ["STOP"]
