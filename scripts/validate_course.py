"""Offline validation for Romeo content using the pinned TheBitLab contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from romeo.simulation.scenario import Scenario

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "course"
SAFE_PATH = re.compile(r"^[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*$")
ACTIVITY_TYPES = {
    "studio-guidato",
    "esercizio-classe",
    "compito-casa",
    "laboratorio",
    "verifica-pratica",
    "verifica-scritta",
    "debug-didattico",
}
DIFFICULTIES = set("ABCDEF")
COURSE_LICENSE = "CC-BY-SA-4.0"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def safe_file(relative: object, *, base: Path = COURSE) -> Path:
    if not isinstance(relative, str) or not SAFE_PATH.fullmatch(relative):
        raise ValueError(f"unsafe portable path: {relative!r}")
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()) or not path.is_file():
        raise ValueError(f"missing bundle file: {relative}")
    return path


def validate_activity(path: Path) -> None:
    data = load(path)
    required = {
        "schema_version",
        "id",
        "titolo",
        "tipo",
        "difficolta",
        "argomenti",
        "consegna",
        "correzione",
        "metriche",
    }
    missing = required - data.keys()
    if missing:
        raise ValueError(f"{path}: missing fields {sorted(missing)}")
    if data["schema_version"] != "1.0" or data["tipo"] not in ACTIVITY_TYPES:
        raise ValueError(f"{path}: unsupported Activity contract")
    if data["difficolta"] not in DIFFICULTIES or not data["argomenti"]:
        raise ValueError(f"{path}: invalid difficulty or topics")
    runtime = data.get("extensions", {}).get("thebitlab.runtime", {})
    if (
        runtime.get("schema_version") != "runtime_activity.v1"
        or runtime.get("runtime_id") != "romeo-sim"
    ):
        raise ValueError(f"{path}: invalid Romeo runtime extension")
    if set(runtime.get("required_capabilities", [])) - {
        "interactive-launch",
        "headless-run",
        "deterministic-grade",
        "artifact-collect",
        "sandbox-plan.v1",
    }:
        raise ValueError(f"{path}: unknown runtime capability")
    config = safe_file(runtime["config"]["path"], base=path.parent)
    config_data = load(config)
    if config_data.get("schema_version") != "romeo.thebitlab.v1":
        raise ValueError(f"{config}: unsupported runtime config")
    Scenario.from_json(safe_file(config_data["scenario"], base=config.parent))
    for asset in data.get("assets", []):
        safe_file(asset["path"], base=path.parent)


def validate() -> int:
    bundle = load(COURSE / "bundle.json")
    required = {
        "schema_version",
        "id",
        "version",
        "title",
        "school_year",
        "target_class",
        "language",
        "authors",
        "license",
        "content",
    }
    if bundle.keys() < required or bundle["schema_version"] != "1.0.0":
        raise ValueError("bundle.json does not implement Course Bundle 1.0.0")
    if bundle["license"] != COURSE_LICENSE:
        raise ValueError(f"bundle.json must use {COURSE_LICENSE}")
    if not (COURSE / "LICENSE.md").is_file():
        raise ValueError("course license notice is missing")
    units = bundle["content"]["units"]
    ids: set[str] = set()
    expected_index = []
    for position, unit in enumerate(units, start=1):
        if unit["id"] in ids:
            raise ValueError(f"duplicate unit id: {unit['id']}")
        ids.add(unit["id"])
        items = []
        for field, item_type in (
            ("activities", "activity"),
            ("materials", "material"),
            ("media", "media"),
            ("handouts", "handout"),
        ):
            for relative in unit.get(field, []):
                item_path = safe_file(relative)
                items.append({"type": item_type, "path": relative})
                if item_type == "activity":
                    validate_activity(item_path)
        expected_index.append(
            {
                "id": unit["id"],
                "title": unit["title"],
                "order": unit.get("order", position),
                "items": items,
            }
        )
    if load(COURSE / "index.json") != {"units": expected_index}:
        raise ValueError("index.json is not the canonical index derived from bundle.json")
    curriculum = load(COURSE / "curriculum.json")
    curriculum_ids = {unit["id"] for year in curriculum["years"] for unit in year["units"]}
    if curriculum_ids != ids:
        raise ValueError("curriculum units do not match bundle units")
    print(f"validated {len(units)} units and {len(units)} activities")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(validate())
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"course validation failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
