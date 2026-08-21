import pytest

from romeo.network.protocol import Command, ProtocolError, error_response, parse_command


@pytest.mark.parametrize("name", ["FORWARD", "BACKWARD", "LEFT", "RIGHT"])
def test_movement_commands_default_to_half_speed(name: str) -> None:
    assert parse_command(name.lower()) == Command(name, (0.5,))


def test_commands_and_serialization() -> None:
    assert parse_command("FORWARD 0.25").to_line() == "FORWARD 0.25"
    assert parse_command("STOP") == Command("STOP")
    assert parse_command("PING") == Command("PING")
    assert parse_command("LOOK 10 175.5") == Command("LOOK", (10.0, 175.5))
    assert parse_command("DRIVE -0.2 0.75") == Command("DRIVE", (-0.2, 0.75))


@pytest.mark.parametrize(
    ("line", "message"),
    [
        ("", "empty command"),
        ("DANCE", "unknown command"),
        ("STOP now", "does not accept"),
        ("LEFT 0.2 extra", "zero or one speed"),
        ("FORWARD fast", "speed must be a number"),
        ("FORWARD nan", "speed must be finite"),
        ("FORWARD 1.1", "speed must be between"),
        ("LOOK 90", "requires pan and tilt"),
        ("LOOK -1 90", "between 0 and 180"),
        ("DRIVE 0.2", "requires left and right"),
        ("DRIVE -1.1 0", "between -1 and 1"),
        ("PING\nSTOP", "exactly one line"),
    ],
)
def test_invalid_commands_have_clear_errors(line: str, message: str) -> None:
    with pytest.raises(ProtocolError, match=message):
        parse_command(line)


def test_error_response_is_one_line() -> None:
    assert error_response("bad\ncommand") == "ERR bad command"
