from main import read_telemetry

class Engine:
    def state(self): return {"schema_version":"romeo.simulation.state.v1","pose":{"x":17},"motors":{},"camera":{},"time":3.5}

def test_restituisce_lo_snapshot_del_engine():
    state=read_telemetry(Engine())
    assert state["pose"]["x"] == 17 and state["time"] == 3.5
