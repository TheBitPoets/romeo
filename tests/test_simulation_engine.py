import math

import pytest

from romeo import Robot
from romeo.backends.factory import create_backend
from romeo.simulation.engine import SimulationEngine
from romeo.simulation.scenario import RectangleObstacle, Scenario


def scenario(**overrides: object) -> Scenario:
    values: dict[str, object] = {
        "schema_version": "romeo.scenario.v1",
        "id": "test-arena",
        "world_width": 4.0,
        "world_height": 3.0,
        "start_x": 1.0,
        "start_y": 1.0,
        "start_heading_degrees": 0.0,
        "robot_radius": 0.1,
        "wheel_base": 0.2,
        "max_wheel_speed": 0.5,
        "obstacles": (),
        "checks": (),
    }
    values.update(overrides)
    return Scenario(**values)  # type: ignore[arg-type]


def test_forward_motion_uses_simulated_clock() -> None:
    engine = SimulationEngine(scenario())
    engine.set_motor_speeds(0.5, 0.5)

    engine.step(2.0)

    assert engine.time == pytest.approx(2.0)
    assert engine.pose.x == pytest.approx(1.5)
    assert engine.pose.y == pytest.approx(1.0)
    assert engine.pose.heading == pytest.approx(0.0)


def test_differential_drive_turns_in_place() -> None:
    engine = SimulationEngine(scenario())
    engine.set_motor_speeds(-0.5, 0.5)

    engine.step(math.pi * 0.2)

    assert engine.pose.x == pytest.approx(1.0)
    assert engine.pose.y == pytest.approx(1.0)
    assert engine.pose.heading == pytest.approx(math.pi / 2)


def test_collision_stops_robot_and_records_event() -> None:
    obstacle = RectangleObstacle(x=1.4, y=0.5, width=0.2, height=1.0)
    engine = SimulationEngine(scenario(obstacles=(obstacle,)))
    engine.set_motor_speeds(1.0, 1.0)

    engine.step(2.0)

    assert engine.collisions == 1
    assert engine.stopped
    assert engine.pose.x < 1.3
    assert any(event.type == "collision" for event in engine.events)


def test_world_boundary_is_a_collision() -> None:
    engine = SimulationEngine(scenario(start_x=3.8))
    engine.set_motor_speeds(1.0, 1.0)

    engine.step(1.0)

    assert engine.collisions == 1
    assert engine.pose.x <= 3.9


def test_state_protocol_is_renderer_neutral() -> None:
    engine = SimulationEngine(scenario())
    engine.set_camera_angles(45.0, 120.0)

    state = engine.state()

    assert state["schema_version"] == "romeo.simulation.state.v1"
    assert state["camera"] == {"pan": 45.0, "tilt": 120.0}
    assert state["world"] == {
        "width": 4.0,
        "height": 3.0,
        "robot_radius": 0.1,
        "obstacles": [],
        "targets": [],
        "checkpoints": [],
    }


def test_simulation_implements_the_same_robot_backend_contract() -> None:
    engine = SimulationEngine(scenario())
    robot = Robot(engine)

    robot.forward(0.5)
    engine.step(1.0)
    robot.stop()

    assert engine.pose.x == pytest.approx(1.25)
    assert engine.stopped


def test_factory_selects_headless_simulator(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ROMEO_BACKEND", "sim")

    backend = create_backend()

    assert isinstance(backend, SimulationEngine)
