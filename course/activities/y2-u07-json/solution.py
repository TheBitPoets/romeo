import json

def encode_state(state):
    """Codifica uno stato come testo JSON."""
    return json.dumps(state)

def decode_state(text):
    """Decodifica e valida type, motors e moving."""
    state = json.loads(text)
    if state.get("type") != "state":
        raise ValueError("type deve essere state")
    if not isinstance(state.get("motors"), list) or len(state["motors"]) != 2:
        raise ValueError("motors deve contenere due valori")
    if not isinstance(state.get("moving"), bool):
        raise ValueError("moving deve essere booleano")
    return state
