from romeo.network.protocol import parse_command

forward = parse_command("FORWARD 0.4")
stop = parse_command("STOP")
assert forward.name == "FORWARD" and forward.arguments == (0.4,)
assert stop.name == "STOP"
print("PROTOCOLLO OK")
