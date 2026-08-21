import pytest
from main import parse_command_line

def test_accetta_comandi_validi():
    assert parse_command_line("FORWARD 0.4") == ("FORWARD", (0.4,))
    assert parse_command_line("STOP") == ("STOP", ())

@pytest.mark.parametrize("line", ["DANCE", "STOP 1", "FORWARD 0.2 0.3", "FORWARD nan"])
def test_rifiuta_comandi_non_validi(line):
    with pytest.raises(ValueError):
        parse_command_line(line)
