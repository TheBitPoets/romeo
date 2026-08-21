import json
from pathlib import Path

from romeo.doctor.models import CheckResult, DiagnosticReport
from romeo.doctor.render import render_json, render_text


def test_text_output_is_student_facing_and_explains_failure() -> None:
    report = DiagnosticReport(
        status="preflight_failed",
        ready=False,
        checks=(CheckResult("i2c", "failed", "Bus I2C non disponibile."),),
    )

    output = render_text(report)

    assert "[ERRORE] I2C" in output
    assert "Che cosa significa:" in output
    assert "Perché serve:" in output
    assert "Possibili cause:" in output
    assert "Controlla:" in output
    assert "Cosa NON fare:" in output
    assert "non è pronto" in output
    assert "Traceback" not in output


def test_json_output_matches_schema() -> None:
    report = DiagnosticReport(
        status="ready",
        ready=True,
        checks=(CheckResult("python", "passed", "È OK", {"version": "3.12"}),),
    )

    payload = json.loads(render_json(report))

    assert payload["schema_version"] == "romeo.hardware_diagnostic.v1"
    assert payload["ready"] is True
    assert payload["checks"][0]["status"] == "passed"
    assert "\\u00c8 OK" in render_json(report)


def test_published_json_schema_matches_report_contract() -> None:
    schema_path = (
        Path(__file__).parents[1]
        / "docs"
        / "hardware"
        / "schemas"
        / "romeo.hardware_diagnostic.v1.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    assert schema["properties"]["schema_version"]["const"] == (
        "romeo.hardware_diagnostic.v1"
    )
    assert set(schema["required"]) == {
        "schema_version",
        "status",
        "ready",
        "checks",
        "calibration",
        "hardware",
    }
    assert schema["properties"]["checks"]["items"]["properties"]["status"]["enum"] == [
        "passed",
        "failed",
        "skipped",
        "warning",
    ]
