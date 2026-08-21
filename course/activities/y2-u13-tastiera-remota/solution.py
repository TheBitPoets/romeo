from romeo.network.keyboard import command_for_key

sequence = [command_for_key(key) for key in ("w", " ")]
assert [command.name for command in sequence] == ["FORWARD", "STOP"]
print("CONTROLLO REMOTO OK")
