from romeo.simulation import Scenario, SimulationEngine

scenario = Scenario.from_mapping({"schema_version": "romeo.scenario.v1", "id": "telemetry"})
state = SimulationEngine(scenario).state()
assert state["schema_version"] == "romeo.simulation.state.v1"
assert {"pose", "motors", "camera", "time"} <= state.keys()
print("TELEMETRIA OK")
