from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path
from types import ModuleType

import pytest

from romeo.integrations.thebitlab.sandbox_worker import execute_behavioral_tests

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_second_year_bundle import UNITS_Y2, activity, runtime_config  # noqa: E402
from y2_contracts import CONTRACTS_Y2  # noqa: E402


def _function_names(source: str) -> set[str]:
    tree = ast.parse(source)
    return {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}


def _run_hidden_function(function: object, arguments: dict[str, object]) -> None:
    signature = inspect.signature(function)  # type: ignore[arg-type]
    monkeypatch = pytest.MonkeyPatch()
    if "monkeypatch" in signature.parameters:
        arguments = {**arguments, "monkeypatch": monkeypatch}
    try:
        function(**arguments)  # type: ignore[operator]
    finally:
        monkeypatch.undo()


def _run_hidden_tests(contract: object) -> None:
    previous_main = sys.modules.get("main")
    main = ModuleType("main")
    exec(contract.solution, main.__dict__)  # type: ignore[attr-defined]
    sys.modules["main"] = main
    namespace: dict[str, object] = {}
    try:
        exec(contract.hidden_tests, namespace)  # type: ignore[attr-defined]
        for name, function in namespace.items():
            if not name.startswith("test_") or not callable(function):
                continue
            parameter_marks = [
                mark
                for mark in getattr(function, "pytestmark", ())
                if mark.name == "parametrize"
            ]
            if not parameter_marks:
                _run_hidden_function(function, {})
                continue
            assert len(parameter_marks) == 1
            mark = parameter_marks[0]
            names = [name.strip() for name in mark.args[0].split(",")]
            for values in mark.args[1]:
                row = values if isinstance(values, tuple) else (values,)
                _run_hidden_function(function, dict(zip(names, row, strict=True)))
    finally:
        if previous_main is None:
            del sys.modules["main"]
        else:
            sys.modules["main"] = previous_main


def test_every_second_year_unit_has_one_explicit_contract() -> None:
    slugs = {unit.slug for unit in UNITS_Y2}

    assert len(slugs) == 23
    assert set(CONTRACTS_Y2) == slugs


@pytest.mark.parametrize("unit", UNITS_Y2, ids=lambda unit: unit.slug)
def test_starter_and_solution_are_import_safe_and_expose_entrypoints(unit: object) -> None:
    contract = CONTRACTS_Y2[unit.slug]  # type: ignore[attr-defined]
    allowed = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Expr)

    for source in (contract.starter, contract.solution):
        tree = ast.parse(source)
        assert all(isinstance(node, allowed) for node in tree.body), unit.slug  # type: ignore[attr-defined]
        assert set(contract.entrypoints) <= _function_names(source)


@pytest.mark.parametrize("unit", UNITS_Y2, ids=lambda unit: unit.slug)
def test_hidden_fixture_is_specific_and_syntactically_valid(unit: object) -> None:
    contract = CONTRACTS_Y2[unit.slug]  # type: ignore[attr-defined]
    tree = ast.parse(contract.hidden_tests)
    tests = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]

    assert tests
    assert "main" in contract.hidden_tests
    assert not any(marker in contract.hidden_tests for marker in unit.markers)  # type: ignore[attr-defined]


@pytest.mark.parametrize("index,unit", enumerate(UNITS_Y2, start=1), ids=lambda value: str(value))
def test_activity_and_runtime_config_delegate_tests_to_the_sandbox_broker(
    index: int, unit: object
) -> None:
    generated_activity = activity(index, unit)  # type: ignore[arg-type]
    generated_config = runtime_config(unit)  # type: ignore[arg-type]
    assets = generated_activity["assets"]

    assert any(
        asset["path"] == "behavioral_tests.py" and asset["visibility"] == "grading"
        for asset in assets
    )
    assert generated_config["stdout_checks"] == []
    assert generated_config["behavioral_tests"] == {
        "path": "behavioral_tests.py",
        "entrypoints": list(CONTRACTS_Y2[unit.slug].entrypoints),  # type: ignore[attr-defined]
        "execution_boundary": "thebitlab-sandbox-broker",
    }


@pytest.mark.parametrize("unit", UNITS_Y2, ids=lambda unit: unit.slug)
def test_reference_solution_defines_callable_entrypoints(unit: object) -> None:
    contract = CONTRACTS_Y2[unit.slug]  # type: ignore[attr-defined]
    namespace: dict[str, object] = {}

    exec(compile(contract.solution, unit.slug, "exec"), namespace)  # type: ignore[attr-defined]

    assert all(callable(namespace[name]) for name in contract.entrypoints)
    _run_hidden_tests(contract)


@pytest.mark.parametrize("unit", UNITS_Y2, ids=lambda unit: unit.slug)
def test_reference_solution_passes_real_sandbox_worker(unit: object, tmp_path: Path) -> None:
    contract = CONTRACTS_Y2[unit.slug]  # type: ignore[attr-defined]
    source = tmp_path / "main.py"
    fixture = tmp_path / "behavioral_tests.py"
    source.write_text(contract.solution, encoding="utf-8")
    fixture.write_text(contract.hidden_tests, encoding="utf-8")

    result = execute_behavioral_tests(source, fixture)

    assert result["exit_code"] == 0, result
    assert result["tests"]
    assert all(test["passed"] for test in result["tests"]), result  # type: ignore[index]

    source.write_text(contract.starter, encoding="utf-8")
    starter_result = execute_behavioral_tests(source, fixture)

    assert any(not test["passed"] for test in starter_result["tests"]), starter_result  # type: ignore[index]
