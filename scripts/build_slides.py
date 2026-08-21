#!/usr/bin/env python3
"""Validate and build Romeo Marp teaching decks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SLIDES_ROOT = ROOT / "slides" / "romeo"
MODULES_ROOT = SLIDES_ROOT / "modules"
DELIVERY = ROOT / "course" / "delivery" / "README.md"
INDEX = SLIDES_ROOT / "README.md"
CURRICULUM = ROOT / "course" / "curriculum.json"
MARP_CLI_VERSION = "4.5.0"
MARP_PACKAGE = f"@marp-team/marp-cli@{MARP_CLI_VERSION}"
DECK_RE = re.compile(r"^(\d{2})_[A-Z0-9_]+\.md$")
EXPECTED = tuple(f"{i:02d}" for i in range(10))


def decks() -> list[Path]:
    return sorted(p for p in MODULES_ROOT.glob("*.md") if DECK_RE.match(p.name))


def front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return "" if end < 0 else text[4:end]


def validate_sources() -> None:
    errors: list[str] = []
    found = decks()
    numbers = tuple(p.name[:2] for p in found)
    if numbers != EXPECTED:
        errors.append(f"expected Romeo decks 00..09, found {numbers}")

    curriculum = json.loads(CURRICULUM.read_text(encoding="utf-8"))
    year_counts = {int(year["year"]): len(year["units"]) for year in curriculum["years"]}
    if year_counts != {1: 20, 2: 23}:
        errors.append(f"expected curriculum unit counts {{1: 20, 2: 23}}, found {year_counts}")

    slide_index = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
    delivery = DELIVERY.read_text(encoding="utf-8") if DELIVERY.exists() else ""
    for deck in found:
        text = deck.read_text(encoding="utf-8")
        fm = front_matter(text)
        if not fm or not re.search(r"(?m)^marp:\s*true\s*$", fm):
            errors.append(f"{deck}: missing Marp front matter")
        if "obiettivi" not in text.lower():
            errors.append(f"{deck}: missing objectives")
        if "checkpoint" not in text.lower():
            errors.append(f"{deck}: missing checkpoint")
        rel = f"modules/{deck.name}"
        if rel not in slide_index:
            errors.append(f"slides/romeo/README.md: missing {rel}")
        full_rel = f"slides/romeo/{rel}"
        if full_rel not in delivery:
            errors.append(f"course/delivery/README.md: missing {full_rel}")

    required = [
        "docs/student/index.md",
        "docs/teacher/index.md",
        "docs/hardware/safety.md",
        "docs/hardware/preflight.md",
        "docs/hardware/commissioning.md",
    ]
    for target in required:
        if not (ROOT / target).exists():
            errors.append(f"missing authoritative delivery target {target}")

    if "romeo-doctor" not in (ROOT / "docs" / "hardware" / "preflight.md").read_text(encoding="utf-8"):
        errors.append("preflight documentation no longer records the romeo-doctor boundary")

    if errors:
        raise SystemExit("Romeo delivery validation failed:\n- " + "\n- ".join(errors))


def generated_path(source: Path, fmt: str) -> Path:
    return source.with_suffix(f".{fmt}")


def run_marp(output_dir: Path, fmt: str, browser: str) -> None:
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("npx not found")
    sources = decks()
    generated = [generated_path(source, fmt) for source in sources]
    output_dir.mkdir(parents=True, exist_ok=True)
    for path in generated:
        path.unlink(missing_ok=True)

    parallel = "1" if fmt == "pptx" else "4"
    cmd = [npx, "--yes", MARP_PACKAGE, "--html", "--allow-local-files", "--parallel", parallel]
    if fmt == "pdf":
        cmd.extend(["--pdf", "--pdf-outlines", "--browser", browser])
    elif fmt == "pptx":
        cmd.extend(["--pptx", "--browser", browser])
    elif fmt != "html":
        raise ValueError(fmt)
    cmd.extend(str(path.relative_to(ROOT)) for path in sources)

    try:
        subprocess.run(cmd, cwd=ROOT, check=True)
        for source, built in zip(sources, generated):
            if not built.exists():
                raise SystemExit(f"missing generated artifact {built}")
            target = output_dir / source.relative_to(SLIDES_ROOT).with_suffix(f".{fmt}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(built), str(target))
    finally:
        for path in generated:
            path.unlink(missing_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(output: Path, formats: list[str]) -> None:
    artifacts = []
    for path in sorted(output.rglob("*")):
        if path.is_file() and path.name not in {"MANIFEST.json", "SHA256SUMS.txt"}:
            artifacts.append({"path": path.relative_to(output).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size})
    sources = [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha256(p)} for p in decks()]
    manifest = {
        "schema": "thebitpoets.course-slides-artifact.v1",
        "course": "romeo-python-robotics",
        "curriculum_schema": "romeo.curriculum.v1",
        "curriculum_units": {"year1": 20, "year2": 23},
        "marp_cli": MARP_CLI_VERSION,
        "commit": os.environ.get("SOURCE_SHA") or os.environ.get("GITHUB_SHA"),
        "formats": formats,
        "source_decks": sources,
        "artifacts": artifacts,
    }
    (output / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "SHA256SUMS.txt").write_text("".join(f"{item['sha256']}  {item['path']}\n" for item in artifacts), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "romeo-slides")
    parser.add_argument("--formats", default="html,pdf,pptx")
    parser.add_argument("--browser", default="chrome")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    validate_sources()
    if args.check_only:
        print(f"OK: 10 macro decks cover curriculum 20+23 units; Marp {MARP_CLI_VERSION}")
        return 0

    formats = [part.strip() for part in args.formats.split(",") if part.strip()]
    invalid = set(formats) - {"html", "pdf", "pptx"}
    if invalid:
        raise SystemExit(f"unsupported formats: {sorted(invalid)}")
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for fmt in formats:
        run_marp(output / fmt, fmt, args.browser)
    write_manifest(output, formats)
    print(f"Built {len(decks())} Romeo decks -> {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
