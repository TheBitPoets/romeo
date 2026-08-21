from romeo.network.protocol import parse_command

def parse_command_line(line):
    """Valida una riga Romeo/1 e restituisce nome e argomenti."""
    command = parse_command(line)
    return command.name, command.arguments
