"""Human and machine-readable rendering for Romeo Doctor."""

from __future__ import annotations

import json

from romeo.doctor.messages import CHECK_HELP
from romeo.doctor.models import DiagnosticReport

_MARKERS = {
    "passed": "OK",
    "failed": "ERRORE",
    "warning": "AVVISO",
    "skipped": "SALTATO",
}


def render_json(report: DiagnosticReport) -> str:
    """Serialize a report using strict JSON (NaN is never accepted)."""

    return json.dumps(
        report.to_dict(), ensure_ascii=True, indent=2, sort_keys=True, allow_nan=False
    )


def render_text(report: DiagnosticReport) -> str:
    """Render concise results and educational help for failed checks."""

    lines = ["Romeo pre-flight", ""]
    for check in report.checks:
        help_item = CHECK_HELP.get(check.id)
        label = help_item.label if help_item else check.id.replace("_", " ").title()
        lines.append(f"[{_MARKERS[check.status]}] {label}: {check.detail}")
        if check.status != "failed" or help_item is None:
            continue
        lines.extend(
            [
                "",
                "Che cosa significa:",
                f"Romeo stava controllando {help_item.component}.",
                "",
                "Perché serve:",
                help_item.purpose,
                "",
                "Possibili cause:",
                *(f"- {cause}" for cause in help_item.causes),
                "",
                "Controlla:",
                *(f"- {step}" for step in help_item.verify),
                "",
                "Cosa NON fare:",
                f"- {help_item.avoid}.",
            ]
        )
    lines.extend(
        [
            "",
            "Romeo è pronto."
            if report.ready
            else "Romeo non è pronto: correggi gli errori prima di usarlo.",
        ]
    )
    return "\n".join(lines)
