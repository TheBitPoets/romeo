"""Verify Romeo fails closed through the real TheBitLab student runtime path."""

# ruff: noqa: I001 -- TheBitLab is imported after deliberate sys.path injection.

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import sys
import tempfile
from collections.abc import Iterator, Mapping
from contextlib import contextmanager

from romeo.integrations.thebitlab.runtime_record import (
    load_runtime_image_record,
    validate_digest_pinned_image,
)

DEFAULT_RUNTIME_RECORD = (
    pathlib.Path(__file__).resolve().parents[1]
    / "docs"
    / "release"
    / "runtime-image-current.env"
)


@contextmanager
def temporary_environment(changes: Mapping[str, str | None]) -> Iterator[None]:
    previous = {name: os.environ.get(name) for name in changes}
    try:
        for name, value in changes.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        yield
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def assignment_fixture(romeo_root: pathlib.Path, root: pathlib.Path) -> dict[str, object]:
    slug = "y1-u08-avanti-indietro"
    source = romeo_root / "course" / "activities" / slug
    activity_dir = root / "activities" / slug
    workspace = root / "workspaces" / slug
    shutil.copytree(source, activity_dir)
    workspace.mkdir(parents=True)
    shutil.copy2(source / "solution.py", workspace / "main.py")
    activity = json.loads((activity_dir / "activity.json").read_text(encoding="utf-8"))
    return {
        "assignment_id": f"fail-closed-{slug}",
        "activity_id": activity["id"],
        "student_id": "diagnostic",
        "activity": {"path": f"activities/{slug}/activity.json"},
        "workspace": {"path": f"workspaces/{slug}"},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--thebitlab-root", type=pathlib.Path, required=True)
    parser.add_argument("--romeo-root", type=pathlib.Path, required=True)
    parser.add_argument("--runtime-record", type=pathlib.Path, default=DEFAULT_RUNTIME_RECORD)
    parser.add_argument(
        "--image",
        help="immutable override; defaults to ROMEO_SANDBOX_IMAGE from the release record",
    )
    arguments = parser.parse_args()

    runtime_record = load_runtime_image_record(arguments.runtime_record)
    approved_image = validate_digest_pinned_image(
        arguments.image or runtime_record.sandbox_image
    )

    sys.path.insert(0, str(arguments.thebitlab_root.resolve(strict=True)))
    from scripts import student_runtime

    from romeo.integrations.thebitlab.plugin import RomeoRuntimePlugin

    fallback_calls: list[str] = []
    original_run = RomeoRuntimePlugin.run

    def forbidden_run(self, request):  # type: ignore[no-untyped-def]
        del self, request
        fallback_calls.append("run")
        raise AssertionError("plugin.run() process fallback was used")

    RomeoRuntimePlugin.run = forbidden_run  # type: ignore[method-assign,assignment]
    cases: dict[str, dict[str, str | None]] = {
        "image_missing": {"ROMEO_SANDBOX_IMAGE": None, "DOCKER_HOST": None},
        "image_invalid": {"ROMEO_SANDBOX_IMAGE": "romeo-runtime:latest", "DOCKER_HOST": None},
        "broker_unavailable": {
            "ROMEO_SANDBOX_IMAGE": approved_image,
            "DOCKER_HOST": "tcp://127.0.0.1:1",
        },
    }
    results: list[dict[str, object]] = []
    try:
        for name, environment in cases.items():
            with tempfile.TemporaryDirectory(prefix=f"romeo-{name}-") as temporary:
                root = pathlib.Path(temporary)
                assignment = assignment_fixture(arguments.romeo_root, root)
                with temporary_environment(environment):
                    report = student_runtime.run_runtime_assignment(
                        assignment,
                        root=root,
                        timeout_seconds=5,
                    )
            runtime = report.get("runtime") if isinstance(report.get("runtime"), dict) else {}
            metadata = (
                runtime.get("metadata") if isinstance(runtime.get("metadata"), dict) else {}
            )
            accepted = report.get("passed") is True or metadata.get("authoritative") is True
            if accepted:
                raise RuntimeError(f"{name} unexpectedly allowed authoritative grading")
            results.append(
                {
                    "case": name,
                    "passed": report.get("passed"),
                    "status": report.get("status"),
                    "requested_backend": runtime.get("requested_backend"),
                    "effective_backend": runtime.get("backend"),
                    "authoritative": metadata.get("authoritative"),
                    "execution_isolation": metadata.get("execution_isolation"),
                }
            )
    finally:
        RomeoRuntimePlugin.run = original_run  # type: ignore[method-assign]

    if fallback_calls:
        raise RuntimeError(f"plugin.run() fallback observed {len(fallback_calls)} time(s)")
    print(
        json.dumps(
            {
                "status": "passed",
                "plugin_run_fallback_calls": 0,
                "runtime_image": approved_image,
                "runtime_source_sha": runtime_record.runtime_source_sha,
                "thebitlab_broker_sha": runtime_record.thebitlab_broker_sha,
                "cases": results,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
