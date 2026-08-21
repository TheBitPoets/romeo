import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from romeo.integrations.thebitlab import create_plugin
from romeo.integrations.thebitlab.worker import execute_submission

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "course"


def test_course_declares_the_selected_license() -> None:
    bundle = json.loads((COURSE / "bundle.json").read_text(encoding="utf-8"))

    assert bundle["license"] == "CC-BY-SA-4.0"
    assert "CC BY-SA 4.0" in (COURSE / "LICENSE.md").read_text(encoding="utf-8")
    assert (ROOT / "LICENSE").read_text(encoding="utf-8").startswith(
        "                                 Apache License"
    )


def test_first_year_bundle_validates_offline() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/validate_course.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "43 units and 43 activities" in completed.stdout


@pytest.mark.parametrize(
    "activity_directory",
    sorted((COURSE / "activities").glob("y*-*")),
    ids=lambda path: path.name,
)
def test_teacher_solution_passes_deterministic_grading(
    activity_directory: Path, tmp_path: Path
) -> None:
    if activity_directory.name.startswith("y2-"):
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        shutil.copyfile(activity_directory / "solution.py", workspace / "main.py")
        request = {
            "schema_version": "runtime_request.v1",
            "runtime_id": "romeo-sim",
            "activity_id": activity_directory.name,
            "assignment_id": "teacher-solution",
            "student_id": "ci",
            "paths": {
                "activity": str(activity_directory.resolve()),
                "workspace": str(workspace.resolve()),
                "config": str((activity_directory / "runtime-config.json").resolve()),
            },
            "submission_artifacts": [
                {
                    "id": "main",
                    "path": "main.py",
                    "media_type": "text/x-python",
                    "required": True,
                }
            ],
            "timeout_seconds": 10,
            "metadata": {},
        }

        result = create_plugin().run(request)

        assert result["status"] == "passed", result
        assert result["metadata"]["score"] == 10.0
        return

    result = execute_submission(
        activity_directory / "solution.py",
        activity_directory / "scenario.json",
        max_simulation_seconds=30,
    )

    assert result["student_error"] is None
    assert result["grade"]["passed"] is True
    assert result["grade"]["score"] == 10.0
