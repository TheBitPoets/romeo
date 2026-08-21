import json
from pathlib import Path

import pytest

from romeo.simulation.scenario import SCENARIO_SCHEMA, Scenario


def test_scenario_uses_documented_defaults() -> None:
    scenario = Scenario.from_mapping({"schema_version": SCENARIO_SCHEMA, "id": "empty-arena"})

    assert (scenario.world_width, scenario.world_height) == (4.0, 3.0)
    assert (scenario.start_x, scenario.start_y, scenario.start_heading_degrees) == (0.5, 0.5, 0.0)
    assert (scenario.robot_radius, scenario.wheel_base, scenario.max_wheel_speed) == (
        0.12,
        0.18,
        0.5,
    )
    assert scenario.obstacles == ()
    assert scenario.checks == ()


def test_scenario_parses_obstacles_and_data_driven_checks() -> None:
    scenario = Scenario.from_mapping(
        {
            "schema_version": SCENARIO_SCHEMA,
            "id": "reach-school",
            "world_width": 6,
            "world_height": 5,
            "start_x": 1,
            "start_y": 1.5,
            "start_heading_degrees": 90,
            "robot_radius": 0.1,
            "wheel_base": 0.2,
            "max_wheel_speed": 0.7,
            "obstacles": [{"x": 2, "y": 1, "width": 0.5, "height": 2}],
            "checks": [
                {
                    "id": "finish",
                    "name": "Reach the finish area",
                    "type": "position",
                    "parameters": {"target": [5, 4], "tolerance": 0.2},
                }
            ],
        }
    )

    assert scenario.obstacles[0].height == 2.0
    assert scenario.checks[0].type == "position"
    assert scenario.checks[0].parameters["target"] == (5, 4)
    with pytest.raises(TypeError):
        scenario.checks[0].parameters["new"] = 1  # type: ignore[index]


def test_from_json_reads_utf8_file(tmp_path: Path) -> None:
    path = tmp_path / "scenario.json"
    path.write_text(
        json.dumps({"schema_version": SCENARIO_SCHEMA, "id": "città"}), encoding="utf-8"
    )

    assert Scenario.from_json(path).id == "città"


@pytest.mark.parametrize(
    ("update", "message"),
    [
        ({"schema_version": "romeo.scenario.v2"}, "schema_version"),
        ({"world_width": 0}, "world_width"),
        ({"world_height": float("inf")}, "world_height"),
        ({"max_wheel_speed": True}, "max_wheel_speed"),
        ({"start_x": -1}, "start_x"),
        ({"robot_radius": 2}, "robot_radius"),
        (
            {"obstacles": [{"x": 3.8, "y": 0, "width": 0.3, "height": 1}]},
            "world_width",
        ),
        (
            {
                "checks": [
                    {"id": "one", "name": "One", "type": "position", "parameters": {}},
                    {"id": "one", "name": "Again", "type": "time", "parameters": {}},
                ]
            },
            "duplicate check id",
        ),
    ],
)
def test_invalid_scenarios_are_rejected(update: dict[str, object], message: str) -> None:
    data: dict[str, object] = {"schema_version": SCENARIO_SCHEMA, "id": "invalid"}
    data.update(update)

    with pytest.raises(ValueError, match=message):
        Scenario.from_mapping(data)


def test_json_root_must_be_an_object(tmp_path: Path) -> None:
    path = tmp_path / "array.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="scenario must be an object"):
        Scenario.from_json(path)


def test_missing_file_is_reported() -> None:
    with pytest.raises(FileNotFoundError):
        Scenario.from_json("does-not-exist.json")
