import subprocess
import sys
from pathlib import Path

import pytest

from romeo.integrations.thebitlab.worker import execute_submission

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "course"


def test_first_year_bundle_validates_offline() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/validate_course.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "20 units and 20 activities" in completed.stdout


@pytest.mark.parametrize(
    "activity_directory",
    sorted((COURSE / "activities").glob("y1-*")),
    ids=lambda path: path.name,
)
def test_teacher_solution_passes_deterministic_grading(activity_directory: Path) -> None:
    result = execute_submission(
        activity_directory / "solution.py",
        activity_directory / "scenario.json",
        max_simulation_seconds=30,
    )

    assert result["student_error"] is None
    assert result["grade"]["passed"] is True
    assert result["grade"]["score"] == 10.0
