"""Structured, unit-specific teaching content used by the Course Bundle builders."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LessonContent:
    """Pedagogical elements that must be specific to one lesson."""

    prerequisites: str
    mental_model: str
    example: str
    guided_practice: tuple[str, ...]
    base_exercise: str
    intermediate_exercise: str
    challenge: str
    common_errors: tuple[str, ...]
    self_check: tuple[str, ...]
    accessibility: str
    glossary: tuple[tuple[str, str], ...] = ()


def numbered(items: tuple[str, ...]) -> str:
    """Render a small ordered Markdown list."""

    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def bullets(items: tuple[str, ...]) -> str:
    """Render a small unordered Markdown list."""

    return "\n".join(f"- {item}" for item in items)


def glossary_table(items: tuple[tuple[str, str], ...]) -> str:
    """Render only the vocabulary introduced by the current lesson."""

    if not items:
        return "Nessun termine nuovo oltre a quelli spiegati nell'esempio."
    rows = ["| Termine | Significato in questa lezione |", "| --- | --- |"]
    rows.extend(f"| `{term}` | {meaning} |" for term, meaning in items)
    return "\n".join(rows)
