import pytest

from romeo.simulation.engine import SimulationEngine
from romeo.simulation.grading import grade
from romeo.simulation.headless import TimedCommand, run_schedule
from romeo.simulation.scenario import Scenario, ScenarioCheck


def mission_scenario() -> Scenario:
    return Scenario(
        schema_version="romeo.scenario.v1",
        id="straight-line",
        world_width=3.0,
        world_height=2.0,
        start_x=0.5,
        start_y=1.0,
        start_heading_degrees=0.0,
        robot_radius=0.1,
        wheel_base=0.2,
        max_wheel_speed=0.5,
        obstacles=(),
        checks=(
            ScenarioCheck(
                "target",
                "Raggiunge il target",
                "reach_position",
                {"x": 1.0, "y": 1.0, "tolerance": 0.02, "points": 3},
            ),
            ScenarioCheck(
                "safe",
                "Nessuna collisione",
                "avoid_collisions",
                {"max_collisions": 0, "points": 1},
            ),
            ScenarioCheck(
                "stop",
                "Si ferma",
                "stop_in_zone",
                {"x": 1.0, "y": 1.0, "tolerance": 0.02, "points": 2},
            ),
        ),
    )


def test_headless_schedule_and_grading_are_deterministic() -> None:
    engine = SimulationEngine(mission_scenario())

    run_schedule(
        engine,
        [TimedCommand(0.0, "forward", 0.5), TimedCommand(2.0, "stop")],
        duration=2.0,
    )
    result = grade(engine)

    assert engine.pose.x == pytest.approx(1.0)
    assert result.passed
    assert result.score == 10.0
    assert result.to_mapping()["schema_version"] == "romeo.grade.v1"


def test_failed_check_reduces_weighted_score() -> None:
    engine = SimulationEngine(mission_scenario())
    engine.stop()

    result = grade(engine)

    assert not result.passed
    assert result.score == 1.6667


def test_schedule_rejects_out_of_order_commands() -> None:
    engine = SimulationEngine(mission_scenario())

    with pytest.raises(ValueError, match="sorted"):
        run_schedule(
            engine,
            [TimedCommand(1.0, "forward"), TimedCommand(0.5, "stop")],
            duration=2.0,
        )


def test_repeated_headless_runs_are_identical() -> None:
    commands = [TimedCommand(0.0, "forward", 0.4), TimedCommand(1.25, "left", 0.3)]
    first = run_schedule(SimulationEngine(mission_scenario()), commands, duration=2.5)
    second = run_schedule(SimulationEngine(mission_scenario()), commands, duration=2.5)

    assert first.state() == second.state()
    assert first.event_log() == second.event_log()
