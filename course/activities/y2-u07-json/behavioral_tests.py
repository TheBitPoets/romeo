import json
import pytest
from main import decode_state, encode_state

def test_round_trip_non_hardcoded():
    state = {"type": "state", "motors": [-0.2, 0.7], "moving": True}
    wire = encode_state(state)
    assert isinstance(wire, str) and json.loads(wire) == state
    assert decode_state(wire) == state

@pytest.mark.parametrize("bad", [{"type":"other","motors":[0,0],"moving":False}, {"type":"state","motors":0,"moving":False}, {"type":"state","motors":[0,0],"moving":1}])
def test_valida_i_tipi(bad):
    with pytest.raises(ValueError): decode_state(json.dumps(bad))
