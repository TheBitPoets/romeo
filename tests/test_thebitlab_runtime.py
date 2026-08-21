from __future__ import annotations

import json
import time
import urllib.request
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any

import pytest

from romeo.integrations.thebitlab import create_plugin
from romeo.integrations.thebitlab.worker import execute_submission


def runtime_request(
    tmp_path: Path,
    source: str,
    *,
    timeout_seconds: int = 5,
) -> tuple[dict[str, Any], Path]:
    activity = tmp_path / "activity"
    runtime = activity / "runtime"
    workspace = tmp_path / "workspace"
    runtime.mkdir(parents=True)
    workspace.mkdir()
    activity_path = activity / "activity.json"
    activity_path.write_text("{}", encoding="utf-8")
    scenario = {
        "schema_version": "romeo.scenario.v1",
        "id": "runtime-straight-line",
        "world_width": 3.0,
        "world_height": 2.0,
        "start_x": 0.5,
        "start_y": 1.0,
        "start_heading_degrees": 0.0,
        "robot_radius": 0.1,
        "wheel_base": 0.2,
        "max_wheel_speed": 0.5,
        "obstacles": [],
        "checks": [
            {
                "id": "target",
                "name": "Raggiunge il target",
                "type": "reach_position",
                "parameters": {"x": 1.0, "y": 1.0, "tolerance": 0.02, "points": 2},
            },
            {
                "id": "stop",
                "name": "Si ferma sul target",
                "type": "stop_in_zone",
                "parameters": {"x": 1.0, "y": 1.0, "tolerance": 0.02, "points": 1},
            },
        ],
    }
    (runtime / "scenario.json").write_text(json.dumps(scenario), encoding="utf-8")
    config = {
        "schema_version": "romeo.thebitlab.v1",
        "scenario": "scenario.json",
        "submission_artifact_id": "main",
        "max_simulation_seconds": 10,
    }
    config_path = runtime / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    (workspace / "main.py").write_text(source, encoding="utf-8")
    request = {
        "schema_version": "runtime_request.v1",
        "runtime_id": "romeo-sim",
        "activity_id": "first-movement",
        "assignment_id": "assignment-1",
        "student_id": "student-1",
        "paths": {
            "activity": str(activity_path.resolve()),
            "workspace": str(workspace.resolve()),
            "config": str(config_path.resolve()),
        },
        "submission_artifacts": [
            {
                "id": "main",
                "path": "main.py",
                "media_type": "text/x-python",
                "required": True,
            }
        ],
        "timeout_seconds": timeout_seconds,
        "metadata": {},
    }
    return request, workspace


def test_descriptor_and_probe_follow_runtime_v1() -> None:
    plugin = create_plugin()

    descriptor = plugin.describe()
    probe = plugin.probe()

    assert descriptor["schema_version"] == "runtime_descriptor.v1"
    assert descriptor["runtime_id"] == "romeo-sim"
    assert descriptor["api_version"] == "runtime_plugin.v1"
    assert set(descriptor["capabilities"]) == {
        "interactive-launch",
        "headless-run",
        "deterministic-grade",
        "artifact-collect",
        "sandbox-plan.v1",
    }
    assert probe["schema_version"] == "runtime_probe.v1"
    assert probe["available"] is True
    assert probe["metadata"]["execution_isolation"] == "process-only"
    assert probe["metadata"]["untrusted_submissions_supported"] is False
    assert probe["metadata"]["sandbox_broker_available"] is False


def test_probe_reports_configured_immutable_sandbox_image(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "ROMEO_SANDBOX_IMAGE",
        "ghcr.io/thebitpoets/romeo-runtime@sha256:" + ("c" * 64),
    )

    probe = create_plugin().probe()

    assert probe["metadata"]["sandbox_broker_available"] is True


def test_sandbox_plan_exposes_only_submission_not_grading_data(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    request, _ = runtime_request(tmp_path, "print('student')\n")
    image = "ghcr.io/thebitpoets/romeo-runtime@sha256:" + ("a" * 64)
    monkeypatch.setenv("ROMEO_SANDBOX_IMAGE", image)

    plan = create_plugin().prepare_sandbox(request)

    assert plan["schema_version"] == "runtime_sandbox_plan.v1"
    assert plan["profile"]["image"] == image
    assert plan["inputs"] == [
        {"source": "submission", "artifact_id": "main", "target": "main.py"}
    ]
    serialized = json.dumps(plan)
    assert "scenario.json" not in serialized
    assert "checks" not in serialized


@pytest.mark.parametrize("image", [None, "ghcr.io/thebitpoets/romeo-runtime:latest"])
def test_sandbox_plan_fails_closed_without_immutable_image(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    image: str | None,
) -> None:
    request, _ = runtime_request(tmp_path, "print('student')\n")
    if image is None:
        monkeypatch.delenv("ROMEO_SANDBOX_IMAGE", raising=False)
    else:
        monkeypatch.setenv("ROMEO_SANDBOX_IMAGE", image)

    with pytest.raises(ValueError, match="immutable OCI image"):
        create_plugin().prepare_sandbox(request)


def test_sandbox_finalize_replays_trace_and_ignores_forged_grade(tmp_path: Path) -> None:
    request, workspace = runtime_request(tmp_path, "print('unused')\n")
    sandbox_result = {
        "schema_version": "runtime_sandbox_result.v1",
        "worker_schema": "romeo.command_trace.v1",
        "status": "completed",
        "payload": {
            "schema_version": "romeo.command_trace.v1",
            "commands": [
                {"operation": "motors", "arguments": [0.5, 0.5]},
                {"operation": "wait", "arguments": [2.0]},
                {"operation": "stop", "arguments": []},
            ],
            "stdout": "forged SCORE 10",
            "stderr": "",
            "student_error": None,
            "grade": {"passed": False, "score": 0},
        },
    }

    result = create_plugin().finalize_sandbox(request, sandbox_result)

    assert result["status"] == "passed", result
    assert result["metadata"]["authoritative"] is True
    assert result["metadata"]["score"] == 10.0
    assert (workspace / result["metadata"]["artifacts"][0]["path"]).is_file()


def test_behavioral_plan_and_finalize_use_trusted_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    request, workspace = runtime_request(tmp_path, "def answer(value):\n    return value * 2\n")
    config_path = Path(request["paths"]["config"])
    tests_path = config_path.parent / "behavioral_tests.py"
    tests_path.write_text(
        "from main import answer\n\n"
        "def test_uses_the_argument():\n"
        "    assert answer(3) == 6\n",
        encoding="utf-8",
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["behavioral_tests"] = {
        "path": "behavioral_tests.py",
        "entrypoints": ["answer"],
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")
    image = "ghcr.io/thebitpoets/romeo-runtime@sha256:" + ("b" * 64)
    monkeypatch.setenv("ROMEO_SANDBOX_IMAGE", image)
    plugin = create_plugin()

    plan = plugin.prepare_sandbox(request)

    assert plan["worker_request"]["mode"] == "behavioral-tests"
    assert plan["inputs"] == [
        {"source": "submission", "artifact_id": "main", "target": "main.py"},
        {
            "source": "activity",
            "path": "runtime/behavioral_tests.py",
            "target": "behavioral_tests.py",
        },
    ]
    result = plugin.finalize_sandbox(
        request,
        {
            "schema_version": "runtime_sandbox_result.v1",
            "worker_schema": "romeo.behavioural_result.v1",
            "status": "completed",
            "payload": {
                "schema_version": "romeo.behavioural_result.v1",
                "tests": [
                    {"name": "test_uses_the_argument", "passed": True, "detail": ""}
                ],
                "stdout": "",
                "stderr": "",
            },
        },
    )

    assert result["status"] == "passed"
    assert result["metadata"]["authoritative"] is True
    assert result["metadata"]["score"] == 10.0
    assert (workspace / result["metadata"]["artifacts"][0]["path"]).is_file()


def test_behavioral_finalize_rejects_forged_test_names(tmp_path: Path) -> None:
    request, _ = runtime_request(tmp_path, "def answer():\n    return 42\n")
    config_path = Path(request["paths"]["config"])
    (config_path.parent / "behavioral_tests.py").write_text(
        "def test_real_contract():\n    assert True\n", encoding="utf-8"
    )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["behavioral_tests"] = {
        "path": "behavioral_tests.py",
        "entrypoints": ["answer"],
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")

    result = create_plugin().finalize_sandbox(
        request,
        {
            "schema_version": "runtime_sandbox_result.v1",
            "worker_schema": "romeo.behavioural_result.v1",
            "status": "completed",
            "payload": {
                "schema_version": "romeo.behavioural_result.v1",
                "tests": [{"name": "test_fake", "passed": True, "detail": ""}],
            },
        },
    )

    assert result["status"] == "invalid_payload"
    assert "trusted test manifest" in result["detail"]


def test_installed_package_exposes_official_thebitlab_entry_point() -> None:
    discovered = [
        entry_point
        for entry_point in entry_points(group="thebitlab.runtimes")
        if entry_point.name == "romeo-sim"
    ]

    assert len(discovered) == 1
    plugin = discovered[0].load()()
    assert plugin.describe()["runtime_id"] == "romeo-sim"


@pytest.mark.parametrize(
    "source",
    [
        """from romeo.easy import forward, stop
from time import sleep
forward(0.5)
sleep(2)
stop()
print('missione completata')
""",
        """from romeo import Robot
from time import sleep
robot = Robot()
robot.forward(0.5)
sleep(2)
robot.stop()
""",
    ],
)
def test_headless_run_executes_same_student_apis_deterministically(
    tmp_path: Path,
    source: str,
) -> None:
    request, workspace = runtime_request(tmp_path, source)
    plugin = create_plugin()
    started = time.monotonic()

    result = plugin.run(request)

    assert time.monotonic() - started < 2.0
    assert result["schema_version"] == "runtime_execution.v1"
    assert result["status"] == "passed", result
    assert result["metadata"]["score"] == 10.0
    assert result["metadata"]["authoritative"] is False
    assert result["metadata"]["execution_isolation"] == "process-only"
    assert all(test["passed"] for test in result["tests"])
    assert len(result["metadata"]["artifacts"]) == 5
    for artifact in result["metadata"]["artifacts"]:
        assert not Path(artifact["path"]).is_absolute()
        assert (workspace / artifact["path"]).is_file()


def test_student_exception_is_a_stable_failed_execution(tmp_path: Path) -> None:
    request, _ = runtime_request(tmp_path, "raise RuntimeError('boom')\n")

    result = create_plugin().run(request)

    assert result["status"] == "failed"
    assert result["tests"][0]["name"] == "student program"
    assert "RuntimeError: boom" in result["stderr"]


def test_declarative_stdout_checks_grade_network_labs(tmp_path: Path) -> None:
    request, _ = runtime_request(tmp_path, "print('HTTP 200 JSON OK')\n")
    config_path = Path(request["paths"]["config"])
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["stdout_checks"] = [
        {"name": "Risposta HTTP", "contains": "HTTP 200", "points": 2},
        {"name": "Payload JSON", "contains": "JSON OK", "points": 1},
    ]
    config_path.write_text(json.dumps(config), encoding="utf-8")

    result = create_plugin().run(request)

    assert result["status"] == "failed"  # Geometry fails, output checks pass.
    assert [test["passed"] for test in result["tests"][-2:]] == [True, True]
    assert result["metadata"]["score"] == 5.0


def test_invalid_stdout_check_configuration_is_rejected(tmp_path: Path) -> None:
    request, _ = runtime_request(tmp_path, "print('anything')\n")
    config_path = Path(request["paths"]["config"])
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["stdout_checks"] = [{"name": "", "contains": "OK"}]
    config_path.write_text(json.dumps(config), encoding="utf-8")

    result = create_plugin().run(request)

    assert result["status"] == "invalid_payload"
    assert "name must be non-empty" in result["detail"]


def test_wall_clock_timeout_terminates_busy_submission(tmp_path: Path) -> None:
    request, _ = runtime_request(tmp_path, "while True:\n    pass\n", timeout_seconds=1)

    result = create_plugin().run(request)

    assert result["status"] == "timeout"
    assert "exceeded 1 seconds" in result["detail"]


def test_worker_does_not_inherit_arbitrary_host_secrets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ROMEO_TEST_SECRET", "must-not-reach-student")
    request, _ = runtime_request(
        tmp_path,
        "import os\nprint(os.environ.get('ROMEO_TEST_SECRET', 'not-present'))\n",
    )

    result = create_plugin().run(request)

    assert "must-not-reach-student" not in result["stdout"]
    assert "not-present" in result["stdout"]


def test_artifact_root_symlink_is_rejected(tmp_path: Path) -> None:
    request, workspace = runtime_request(tmp_path, "print('hello')\n")
    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        (workspace / ".romeo").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks are unavailable on this host")

    result = create_plugin().run(request)

    assert result["status"] == "invalid_payload"
    assert "unsafe artifact directory" in result["detail"]
    assert list(outside.iterdir()) == []


def test_invalid_request_is_reported_without_throwing(tmp_path: Path) -> None:
    request, _ = runtime_request(tmp_path, "print('hello')\n")
    request["runtime_id"] = "another-runtime"

    result = create_plugin().run(request)

    assert result["status"] == "invalid_payload"
    assert "runtime_id" in result["detail"]


def test_in_process_worker_runs_do_not_reuse_easy_api_backend(tmp_path: Path) -> None:
    request, workspace = runtime_request(
        tmp_path,
        "from romeo.easy import forward, stop\n"
        "from time import sleep\n"
        "forward(0.5)\n"
        "sleep(2)\n"
        "stop()\n",
    )
    scenario = Path(request["paths"]["config"]).parent / "scenario.json"

    first = execute_submission(workspace / "main.py", scenario, max_simulation_seconds=10)
    second = execute_submission(workspace / "main.py", scenario, max_simulation_seconds=10)

    assert first["grade"]["passed"] is True
    assert second["grade"]["passed"] is True


def test_cleanup_does_not_make_missing_student_stop_pass(tmp_path: Path) -> None:
    request, workspace = runtime_request(
        tmp_path,
        "from romeo.easy import forward\n"
        "from time import sleep\n"
        "forward(0.5)\n"
        "sleep(2)\n",
    )
    scenario = Path(request["paths"]["config"]).parent / "scenario.json"

    result = execute_submission(workspace / "main.py", scenario, max_simulation_seconds=10)

    checks = {check["id"]: check for check in result["grade"]["checks"]}
    assert checks["target"]["passed"] is True
    assert checks["stop"]["passed"] is False
    assert result["state"]["running"] is True


def test_in_process_worker_restores_sys_argv(tmp_path: Path) -> None:
    request, workspace = runtime_request(tmp_path, "print('ok')\n")
    scenario = Path(request["paths"]["config"]).parent / "scenario.json"
    before = list(__import__("sys").argv)

    execute_submission(workspace / "main.py", scenario, max_simulation_seconds=10)

    assert __import__("sys").argv == before


@pytest.mark.parametrize("unsafe_path", ["../scenario.json", "runtime//scenario.json", "C:/x.json"])
def test_runtime_config_rejects_unsafe_paths(tmp_path: Path, unsafe_path: str) -> None:
    request, _ = runtime_request(tmp_path, "print('hello')\n")
    config_path = Path(request["paths"]["config"])
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["scenario"] = unsafe_path
    config_path.write_text(json.dumps(config), encoding="utf-8")

    result = create_plugin().run(request)

    assert result["status"] == "invalid_payload"
    assert "safe relative POSIX path" in result["detail"]


def test_interactive_launch_returns_endpoint_and_close_is_idempotent(tmp_path: Path) -> None:
    request, workspace = runtime_request(tmp_path, "print('viewer')\n")
    plugin = create_plugin()
    if not plugin.probe()["metadata"]["interactive_available"]:
        pytest.skip("Romeo web extra is not installed")

    hijack_marker = workspace / "uvicorn-imported.txt"
    (workspace / "uvicorn.py").write_text(
        f"from pathlib import Path\nPath({str(hijack_marker)!r}).write_text('unsafe')\n",
        encoding="utf-8",
    )
    launch = plugin.launch(request)
    try:
        assert launch["status"] == "started", launch
        with urllib.request.urlopen(launch["endpoint"] + "api/info", timeout=2) as response:
            info = json.load(response)
        assert info["name"] == "Romeo"
        assert not hijack_marker.exists()
    finally:
        if launch.get("session_id"):
            plugin.close(launch["session_id"])
            plugin.close(launch["session_id"])
