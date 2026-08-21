"""Exercise the published Romeo image through the real TheBitLab Docker broker."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any


BROKER_COMMIT = "dcb76f600fa951ba94fffbd355a6c13dfcbfb424"
ACTIVITIES = (
    "y1-u08-avanti-indietro",
    "y2-u07-json",
)


def _load_student_runtime(thebitlab_root: Path) -> ModuleType:
    root = thebitlab_root.resolve(strict=True)
    sys.path.insert(0, str(root))
    from scripts import student_runtime

    return student_runtime


def _run_activity(
    student_runtime: ModuleType,
    *,
    romeo_root: Path,
    temporary_root: Path,
    slug: str,
) -> dict[str, Any]:
    source = romeo_root / "course" / "activities" / slug
    activity_dir = temporary_root / "activities" / slug
    workspace = temporary_root / "workspaces" / slug
    shutil.copytree(source, activity_dir)
    workspace.mkdir(parents=True)
    shutil.copy2(source / "solution.py", workspace / "main.py")

    activity = json.loads((activity_dir / "activity.json").read_text(encoding="utf-8"))
    assignment = {
        "assignment_id": f"runtime-smoke-{slug}",
        "activity_id": activity["id"],
        "student_id": "ci-runtime-smoke",
        "activity": {"path": f"activities/{slug}/activity.json"},
        "workspace": {"path": f"workspaces/{slug}"},
    }
    report = student_runtime.run_runtime_assignment(
        assignment,
        root=temporary_root,
        timeout_seconds=30,
        backend="docker",
    )
    if not report.get("passed"):
        raise RuntimeError(
            f"TheBitLab runtime smoke failed for {slug}: "
            + json.dumps(report, ensure_ascii=False, sort_keys=True)
        )

    runtime = report.get("runtime")
    if not isinstance(runtime, dict) or runtime.get("backend") != "docker":
        raise RuntimeError(f"TheBitLab did not report Docker backend for {slug}")
    metadata = runtime.get("metadata")
    if not isinstance(metadata, dict):
        raise RuntimeError(f"TheBitLab runtime metadata missing for {slug}")
    if metadata.get("authoritative") is not True:
        raise RuntimeError(f"TheBitLab result is not authoritative for {slug}")
    if metadata.get("execution_isolation") != "docker":
        raise RuntimeError(f"Unexpected execution isolation for {slug}: {metadata!r}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--thebitlab-root", type=Path, required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument(
        "--romeo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    arguments = parser.parse_args()

    if "@sha256:" not in arguments.image:
        raise SystemExit("--image must be an immutable OCI reference")
    os.environ["ROMEO_SANDBOX_IMAGE"] = arguments.image

    student_runtime = _load_student_runtime(arguments.thebitlab_root)
    with tempfile.TemporaryDirectory(prefix="romeo-thebitlab-smoke-") as temporary:
        temporary_root = Path(temporary)
        reports = [
            _run_activity(
                student_runtime,
                romeo_root=arguments.romeo_root.resolve(strict=True),
                temporary_root=temporary_root,
                slug=slug,
            )
            for slug in ACTIVITIES
        ]

    print(
        json.dumps(
            {
                "status": "passed",
                "broker_commit": BROKER_COMMIT,
                "image": arguments.image,
                "activities": [report["activity_id"] for report in reports],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
