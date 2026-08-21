from fastapi.testclient import TestClient

from romeo.simulation.engine import SimulationEngine
from romeo.simulation.scenario import SCENARIO_SCHEMA, Scenario
from romeo.web.app import create_app


def engine() -> SimulationEngine:
    return SimulationEngine(
        Scenario.from_mapping({"schema_version": SCENARIO_SCHEMA, "id": "web-test"})
    )


def test_viewer_and_state_endpoint() -> None:
    app = create_app(engine())

    with TestClient(app) as client:
        viewer = client.get("/")
        script = client.get("/static/viewer.js")
        state = client.get("/api/state")

    assert viewer.status_code == 200
    assert "Romeo" in viewer.text
    assert script.status_code == 200
    assert "WebSocket" in script.text
    assert state.json()["schema_version"] == "romeo.simulation.state.v1"
    assert not state.json()["session_running"]


def test_start_stop_and_reset_lifecycle() -> None:
    simulation = engine()
    simulation.set_motor_speeds(0.5, 0.5)
    app = create_app(simulation)

    with TestClient(app) as client:
        assert client.post("/api/simulation/start").json()["status"] == "started"
        assert client.post("/api/simulation/start").json()["status"] == "already_running"
        assert client.post("/api/simulation/stop").json()["status"] == "stopped"
        simulation.step(0.2)
        response = client.post("/api/simulation/reset").json()

    assert response["status"] == "reset"
    assert response["state"]["time"] == 0.0
    assert simulation.stopped


def test_websocket_publishes_versioned_state() -> None:
    app = create_app(engine())

    with TestClient(app) as client, client.websocket_connect("/ws/state") as websocket:
        state = websocket.receive_json()

    assert state["schema_version"] == "romeo.simulation.state.v1"
    assert state["scenario_id"] == "web-test"
