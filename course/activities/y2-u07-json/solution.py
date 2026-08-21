import json

message = {"type": "state", "motors": [0.3, 0.3], "moving": True}
wire = json.dumps(message)
decoded = json.loads(wire)
assert decoded["type"] == "state" and decoded["moving"] is True
print("JSON OK")
