import pytest
from fastapi.testclient import TestClient

from romeo.simulation.engine import SimulationEngine
from romeo.simulation.scenario import SCENARIO_SCHEMA, Scenario
from romeo.web.app import _command_from_payload, create_app


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


def test_status_info_and_openapi_are_documented() -> None:
    app = create_app(engine())

    with TestClient(app) as client:
        status = client.get("/api/status").json()
        info = client.get("/api/info").json()
        openapi = client.get("/openapi.json").json()

    assert status["status"] == "ok"
    assert not status["controller_active"]
    assert info["commands"] == ["forward", "backward", "left", "right", "stop", "look"]
    assert "/api/status" in openapi["paths"]


def test_control_websocket_drives_and_stops_on_disconnect() -> None:
    simulation = engine()
    app = create_app(simulation)

    with TestClient(app) as client:
        with client.websocket_connect("/ws/control") as websocket:
            assert websocket.receive_json()["type"] == "ready"
            websocket.send_json({"command": "forward", "speed": 0.4})
            acknowledgement = websocket.receive_json()
            assert acknowledgement["type"] == "ack"
            assert acknowledgement["command"] == "forward"
            assert (simulation.left_speed, simulation.right_speed) == (0.4, 0.4)

            with client.websocket_connect("/ws/control") as second:
                error = second.receive_json()
                assert error["code"] == "controller_busy"

        assert simulation.stopped
        assert not client.get("/api/status").json()["controller_active"]


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {},
        {"command": "forward", "speed": True},
        {"command": "look", "pan": 90},
        {"command": "dance"},
    ],
)
def test_invalid_websocket_commands_are_rejected(payload: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        _command_from_payload(payload)
