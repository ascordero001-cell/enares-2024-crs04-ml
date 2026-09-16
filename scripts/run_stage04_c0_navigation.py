"""Run the frozen C0/C2 navigation protocol through the Streamlit UI."""

from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from enares.stage04.c0_fixture import (
    C0_AUTOMATION_CASES,
    C3_RETEST_AUTOMATION_CASES,
    AutomatedNavigationCase,
    build_synthetic_catalog,
)


def execute_task(task: AutomatedNavigationCase) -> tuple[float, str, bool]:
    """Exercise the UI mechanics; this does not measure human navigation time."""
    started = perf_counter()
    app = AppTest.from_file(str(ROOT / "app" / "c0_navigation_app.py")).run(timeout=15)
    next(widget for widget in app.selectbox if widget.label == "Módulo").set_value(
        task.module_id
    ).run(timeout=15)
    next(widget for widget in app.selectbox if widget.label == "Dimensión").set_value(
        task.dimension
    ).run(timeout=15)
    next(widget for widget in app.text_input if widget.label == "Buscar indicador").set_value(
        task.query
    ).run(timeout=15)
    broad_result = next(widget for widget in app.selectbox if widget.label == "Resultado")
    if len(broad_result.options) < 2:
        raise AssertionError("the broad query must return plausible alternatives")
    for label, value in (
        ("Tema", task.focus),
        ("Población", task.population),
        ("Periodo", task.period),
        ("Ámbito", task.context),
    ):
        next(widget for widget in app.selectbox if widget.label == label).set_value(
            value
        ).run(timeout=15)
    result = next(widget for widget in app.selectbox if widget.label == "Resultado")
    if result.value is not None:
        raise AssertionError("the result selector must start without a selection")
    if app.code:
        raise AssertionError("indicator_id became visible before explicit confirmation")
    target = next(
        row
        for row in build_synthetic_catalog()
        if row.indicator_id == task.expected_indicator_id
    )
    if len(result.options) != 1:
        raise AssertionError("the semantic facets must identify one candidate")
    result.set_value(target).run(timeout=15)
    if app.code:
        raise AssertionError("indicator_id became visible before confirmation")
    next(button for button in app.button if button.label == "Confirmar indicador").click().run(
        timeout=15
    )
    elapsed = perf_counter() - started
    visible_ids = [element.value for element in app.code]
    found = visible_ids[0] if len(visible_ids) == 1 else ""
    passed = (
        not app.exception
        and found == task.expected_indicator_id
    )
    return elapsed, found, passed


def main() -> None:
    print("task,module,dimension,query,apptest_seconds,result")
    for task in (*C0_AUTOMATION_CASES, *C3_RETEST_AUTOMATION_CASES):
        elapsed, found, passed = execute_task(task)
        status = "PASS" if passed else f"FAIL:{found or 'NO_UNIQUE_RESULT'}"
        print(
            f'{task.task_id},{task.module_id},{task.dimension},"{task.query}",'
            f"{elapsed:.3f},{status}"
        )


if __name__ == "__main__":
    main()
