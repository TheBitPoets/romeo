"""Generate the public Sphinx course catalog from authoritative Course Bundle data."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "course"
DEFAULT_OUTPUT = ROOT / "docs" / "course" / "generated"
PUBLIC_VISIBILITIES = {"student", "public"}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def _text(value: Any, fallback: str = "-") -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _public_assets(activity: dict[str, Any]) -> list[dict[str, Any]]:
    assets = activity.get("assets")
    if not isinstance(assets, list):
        return []
    return [
        item
        for item in assets
        if isinstance(item, dict)
        and str(item.get("visibility") or "").strip() in PUBLIC_VISIBILITIES
    ]


def _runtime(activity: dict[str, Any]) -> tuple[str, list[str]]:
    extensions = activity.get("extensions")
    if not isinstance(extensions, dict):
        return "-", []
    runtime = extensions.get("thebitlab.runtime")
    if not isinstance(runtime, dict):
        return "-", []
    runtime_id = _text(runtime.get("runtime_id"))
    capabilities = _string_list(runtime.get("required_capabilities"))
    return runtime_id, capabilities


def _unit_page(unit: dict[str, Any], activity: dict[str, Any]) -> str:
    title = _text(unit.get("title"), _text(activity.get("title"), "Unità Romeo"))
    objective = _text(unit.get("objective"), _text(activity.get("objective")))
    minutes = unit.get("estimated_minutes")
    difficulty = _text(unit.get("difficulty"), _text(activity.get("difficulty")))
    topics = _string_list(activity.get("topics"))
    prerequisites = _string_list(activity.get("prerequisites"))
    instructions = _text(activity.get("instructions"))
    runtime_id, capabilities = _runtime(activity)
    assets = _public_assets(activity)

    lines = [
        f"# {title}",
        "",
        f"**Obiettivo:** {objective}",
        "",
        f"**Durata stimata:** {minutes if isinstance(minutes, int) else '-'} minuti",
        "",
        f"**Difficoltà:** {difficulty}",
        "",
        "## Prerequisiti",
        "",
    ]
    lines.extend(f"- {item}" for item in prerequisites)
    if not prerequisites:
        lines.append("- Nessun prerequisito specifico oltre alle unità precedenti indicate dal corso.")

    lines.extend(["", "## Concetti", ""])
    lines.extend(f"- {item}" for item in topics)
    if not topics:
        lines.append("- Vedi obiettivo e consegna dell'Activity.")

    lines.extend(
        [
            "",
            "## Consegna sintetica",
            "",
            instructions,
            "",
            "## Runtime",
            "",
            f"- runtime: `{runtime_id}`",
        ]
    )
    lines.extend(f"- capability richiesta: `{item}`" for item in capabilities)

    lines.extend(["", "## Materiali visibili allo studente", ""])
    if assets:
        for asset in assets:
            path = _text(asset.get("path"))
            description = _text(asset.get("description"), _text(asset.get("type")))
            lines.append(f"- `{path}` — {description}")
    else:
        lines.append("- Nessun asset pubblico aggiuntivo dichiarato.")

    lines.extend(
        [
            "",
            "```{admonition} Fonte autorevole",
            ":class: note",
            "Questa pagina è generata dai manifest del Course Bundle. Soluzioni docente, hidden test "
            "e asset di grading non vengono renderizzati nel catalogo pubblico.",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def _year_page(year: dict[str, Any]) -> str:
    year_number = int(year["year"])
    focus = _text(year.get("focus"))
    units = year.get("units")
    if not isinstance(units, list):
        raise ValueError(f"Invalid units for year {year_number}")

    lines = [
        f"# Anno {year_number}",
        "",
        f"**Focus:** {focus}",
        "",
        "| # | Unità | Obiettivo | Min | Diff. |",
        "|---:|---|---|---:|:---:|",
    ]
    paths: list[str] = []
    for unit in units:
        if not isinstance(unit, dict):
            continue
        slug = _text(unit.get("id"))
        order = unit.get("order")
        title = _text(unit.get("title"))
        objective = _text(unit.get("objective"))
        minutes = unit.get("estimated_minutes")
        difficulty = _text(unit.get("difficulty"))
        lines.append(
            f"| {order} | [{title}]({slug}.md) | {objective} | {minutes} | {difficulty} |"
        )
        paths.append(slug)

    lines.extend(["", "```{toctree}", ":hidden:", ":maxdepth: 1", ""])
    lines.extend(paths)
    lines.extend(["```", ""])
    return "\n".join(lines)


def generate(output: Path = DEFAULT_OUTPUT) -> int:
    curriculum = _load_json(COURSE / "curriculum.json")
    years = curriculum.get("years")
    if not isinstance(years, list):
        raise ValueError("curriculum.years must be a list")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    total = 0
    year_pages: list[str] = []
    for year in years:
        if not isinstance(year, dict):
            continue
        year_number = int(year["year"])
        year_name = f"year-{year_number}"
        year_pages.append(year_name)
        (output / f"{year_name}.md").write_text(_year_page(year), encoding="utf-8")

        units = year.get("units")
        if not isinstance(units, list):
            continue
        for unit in units:
            if not isinstance(unit, dict):
                continue
            activity_relative = _text(unit.get("activity"), "")
            if not activity_relative:
                raise ValueError(f"Missing activity path for {unit.get('id')}")
            activity = _load_json(COURSE / activity_relative)
            slug = _text(unit.get("id"), "")
            if not slug:
                raise ValueError("Unit without id")
            (output / f"{slug}.md").write_text(_unit_page(unit, activity), encoding="utf-8")
            total += 1

    index_lines = [
        "# Catalogo delle unità",
        "",
        "Queste pagine sono generate automaticamente dai manifest del Course Bundle.",
        "",
        "```{toctree}",
        ":maxdepth: 2",
        "",
        *year_pages,
        "```",
        "",
    ]
    (output / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
    return total


def main() -> None:
    total = generate()
    print(f"Generated documentation for {total} Romeo course units.")


if __name__ == "__main__":
    main()
