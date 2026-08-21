from romeo.network.keyboard import command_for_key

def commands_for_keys(keys):
    """Traduce i tasti e termina sempre la sequenza con STOP."""
    commands = []
    for key in keys:
        try:
            command = command_for_key(key.lower())
        except ValueError:
            continue
        if command is not None:
            commands.append(command.name)
    if not commands or commands[-1] != "STOP":
        commands.append("STOP")
    return commands
