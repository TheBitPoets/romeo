def read_telemetry(engine):
    """Legge e valida uno snapshot dal simulation engine."""
    state = engine.state()
    if state.get("schema_version") != "romeo.simulation.state.v1":
        raise ValueError("schema telemetria inatteso")
    required = {"pose", "motors", "camera", "time"}
    if not required <= state.keys():
        raise ValueError("telemetria incompleta")
    return state
