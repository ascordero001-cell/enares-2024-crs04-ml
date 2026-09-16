from __future__ import annotations

import re

from enares.stage04.c0_fixture import (
    ALLOWED_HELP,
    C0_TASKS,
    CATALOG_SIZE,
    HUMAN_TIME_LIMIT_SECONDS,
    MODULE_THEMES,
    PER_MODULE,
    build_synthetic_catalog,
)
from enares.stage04.catalog_navigation import CatalogLocator, filter_catalog
from scripts.run_stage04_c0_navigation import execute_task


def test_c0_fixture_has_exactly_516_distributed_synthetic_indicators() -> None:
    catalog = build_synthetic_catalog()

    assert len(catalog) == CATALOG_SIZE == 516
    assert all(row.synthetic is True for row in catalog)
    assert {
        module_id: sum(row.module_id == module_id for row in catalog)
        for module_id in MODULE_THEMES
    } == dict.fromkeys(MODULE_THEMES, PER_MODULE)
    assert len({row.indicator_id for row in catalog}) == CATALOG_SIZE


def test_c0_fixture_exercises_difficult_and_near_duplicate_labels() -> None:
    labels = [row.label for row in build_synthetic_catalog()]

    assert sum(len(label) >= 120 for label in labels) >= 500
    assert sum("((" in label or ") —" in label for label in labels) == CATALOG_SIZE
    near_duplicate_families = {re.sub(r"\d{3}", "NNN", label) for label in labels}
    assert len(near_duplicate_families) == 12


def test_c0_and_c2_protocol_is_frozen_before_execution() -> None:
    assert HUMAN_TIME_LIMIT_SECONDS == 90.0
    assert ALLOWED_HELP == "Solo el texto de la tarea; sin conocer el ID y sin ayuda externa."
    assert len(C0_TASKS) == 7
    assert {task.module_id for task in C0_TASKS} == set(MODULE_THEMES)
    assert sum(task.dimension == "Departamento" for task in C0_TASKS) == 1
    assert all(task.query and task.expected_indicator_id for task in C0_TASKS)


def test_c0_seven_tasks_run_through_streamlit_navigation() -> None:
    for task in C0_TASKS:
        elapsed, found, passed = execute_task(task)

        assert found == task.expected_indicator_id
        assert elapsed <= HUMAN_TIME_LIMIT_SECONDS
        assert passed


def test_c0_rejects_any_non_synthetic_locator() -> None:
    real = CatalogLocator(
        "3.1", "REAL", "No permitido", "Nacional", "Total", synthetic=False
    )
    try:
        filter_catalog([real], module_id="3.1", dimension="Nacional", query="permitido")
    except ValueError as error:
        assert "synthetic=true" in str(error)
    else:
        raise AssertionError("C0 must reject non-synthetic locators")


def test_c0_search_is_accent_and_case_insensitive() -> None:
    matches = filter_catalog(
        build_synthetic_catalog(),
        module_id="3.3",
        dimension="Nacional",
        query="PSICOLOGICA ESCUELA REPETIDO 033",
    )
    assert [row.indicator_id for row in matches] == ["SYN_C0_33_033"]
