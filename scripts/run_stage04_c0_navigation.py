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
    C0_TASKS,
    HUMAN_TIME_LIMIT_SECONDS,
    NavigationTask,
)


def execute_task(task: NavigationTask) -> tuple[float, str, bool]:
    """Execute the same start-to-finish UI path frozen for C0 and C2."""
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
    result = next(widget for widget in app.selectbox if widget.label == "Resultado")
    result.set_value(result.value).run(timeout=15)
    elapsed = perf_counter() - started
    visible_ids = [element.value for element in app.code]
    found = visible_ids[0] if len(visible_ids) == 1 else ""
    passed = (
        not app.exception
        and found == task.expected_indicator_id
        and elapsed <= HUMAN_TIME_LIMIT_SECONDS
    )
    return elapsed, found, passed


def main() -> None:
    print("task,module,dimension,query,elapsed_seconds,limit_seconds,result")
    for task in C0_TASKS:
        elapsed, found, passed = execute_task(task)
        status = "PASS" if passed else f"FAIL:{found or 'NO_UNIQUE_RESULT'}"
        print(
            f'{task.task_id},{task.module_id},{task.dimension},"{task.query}",'
            f"{elapsed:.3f},{HUMAN_TIME_LIMIT_SECONDS:.0f},{status}"
        )


if __name__ == "__main__":
    main()
