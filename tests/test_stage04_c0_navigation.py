from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

from enares.stage04.c0_fixture import (
    ALLOWED_HELP,
    C0_AUTOMATION_CASES,
    C0_TASKS,
    C3_RETEST_AUTOMATION_CASES,
    C3_RETEST_TASKS,
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
    repeated_prefixes = [label.split(" (periodo sintético", 1)[0] for label in labels]
    assert len(set(repeated_prefixes)) < len(repeated_prefixes)


def test_c0_and_c2_protocol_is_frozen_before_execution() -> None:
    assert HUMAN_TIME_LIMIT_SECONDS == 90.0
    assert ALLOWED_HELP == "Solo el texto de la tarea; sin conocer el ID y sin ayuda externa."
    assert len(C0_TASKS) == 7
    assert len(C0_AUTOMATION_CASES) == 7
    assert {case.module_id for case in C0_AUTOMATION_CASES} == set(MODULE_THEMES)
    assert sum(case.dimension == "Departamento" for case in C0_AUTOMATION_CASES) == 1
    assert {task.task_id for task in C0_TASKS} == {
        case.task_id for case in C0_AUTOMATION_CASES
    }
    assert all(task.prompt for task in C0_TASKS)


def test_human_prompts_do_not_reveal_automation_targets() -> None:
    tasks = {task.task_id: task for task in C0_TASKS}
    for case in C0_AUTOMATION_CASES:
        prompt = tasks[case.task_id].prompt
        sequence = case.expected_indicator_id.rsplit("_", 1)[-1]

        assert case.expected_indicator_id not in prompt
        assert sequence not in prompt
        assert case.query.casefold() != prompt.casefold()


def test_c0_seven_tasks_run_through_streamlit_navigation() -> None:
    for task in C0_AUTOMATION_CASES:
        elapsed, found, passed = execute_task(task)

        assert found == task.expected_indicator_id
        assert elapsed <= HUMAN_TIME_LIMIT_SECONDS
        assert passed


def test_each_automated_query_offers_plausible_candidates() -> None:
    catalog = build_synthetic_catalog()
    for case in C0_AUTOMATION_CASES:
        matches = filter_catalog(
            catalog,
            module_id=case.module_id,
            dimension=case.dimension,
            query=case.query,
        )
        assert len(matches) >= 2
        assert case.expected_indicator_id in {row.indicator_id for row in matches}


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
        query="ACOMPAÑAMIENTO",
    )
    assert "SYN_C0_33_033" in {row.indicator_id for row in matches}


def test_free_search_prioritizes_semantic_match_over_repeated_module_title() -> None:
    matches = filter_catalog(
        build_synthetic_catalog(),
        module_id="3.1",
        dimension="Nacional",
        query="corresponsabilidad",
    )

    assert len(matches) > 10
    assert matches[0].focus == "corresponsabilidad cotidiana"
    first_generic = next(
        index
        for index, row in enumerate(matches)
        if row.focus != "corresponsabilidad cotidiana"
    )
    assert all(
        row.focus == "corresponsabilidad cotidiana"
        for row in matches[:first_generic]
    )


def test_relevance_ties_preserve_catalog_order_instead_of_sorting_population() -> None:
    catalog = build_synthetic_catalog()
    matches = filter_catalog(
        catalog,
        module_id="3.5",
        dimension="Nacional",
        query="respuesta",
    )
    tied = [row for row in matches if row.focus == "respuesta institucional"]
    canonical = [
        row
        for row in catalog
        if row.module_id == "3.5"
        and row.dimension == "Nacional"
        and row.focus == "respuesta institucional"
    ]

    assert [row.indicator_id for row in tied] == [
        row.indicator_id for row in canonical
    ]


def test_facets_narrow_progressively_in_the_streamlit_route() -> None:
    root = Path(__file__).resolve().parents[1]
    app = AppTest.from_file(str(root / "app" / "c0_navigation_app.py")).run(
        timeout=15
    )
    next(widget for widget in app.selectbox if widget.label == "Módulo").set_value(
        "3.5"
    ).run(timeout=15)
    next(
        widget for widget in app.text_input if widget.label == "Buscar indicador"
    ).set_value("respuesta").run(timeout=15)

    focus_widget = next(
        widget for widget in app.selectbox if widget.label == "Tema"
    )
    focus_widget.set_value("respuesta institucional").run(timeout=15)
    population_widget = next(
        widget for widget in app.selectbox if widget.label == "Población"
    )
    assert "hogares con persona adulta de referencia" in population_widget.options

    population_widget.set_value("hogares con persona adulta de referencia").run(
        timeout=15
    )
    period_widget = next(
        widget for widget in app.selectbox if widget.label == "Periodo"
    )
    period_widget.set_value("últimos 12 meses").run(timeout=15)
    context_widget = next(
        widget for widget in app.selectbox if widget.label == "Ámbito"
    )
    context_widget.set_value("ámbito rural").run(timeout=15)

    result = next(widget for widget in app.selectbox if widget.label == "Resultado")
    assert len(result.options) == 1
    assert "hogares con persona adulta de referencia" in result.options[0]


def test_free_search_finds_visible_module_words_without_facets() -> None:
    matches = filter_catalog(
        build_synthetic_catalog(),
        module_id="3.2",
        dimension="Nacional",
        query="violencia",
    )

    assert len(matches) == 80


def test_c0_fixture_excludes_population_outside_crs04_authority() -> None:
    catalog = build_synthetic_catalog()

    assert all("9 a 11" not in row.population for row in catalog)
    assert all("9 a 11" not in row.label for row in catalog)


def test_c3_retest_uses_seven_previously_unused_targets() -> None:
    original_targets = {case.expected_indicator_id for case in C0_AUTOMATION_CASES}
    retest_targets = {
        case.expected_indicator_id for case in C3_RETEST_AUTOMATION_CASES
    }

    assert len(C3_RETEST_TASKS) == len(C3_RETEST_AUTOMATION_CASES) == 7
    assert not original_targets & retest_targets
    assert {case.module_id for case in C3_RETEST_AUTOMATION_CASES} == set(
        MODULE_THEMES
    )
    assert sum(
        case.dimension == "Departamento" for case in C3_RETEST_AUTOMATION_CASES
    ) == 1


def test_semantic_facets_reduce_each_c3_task_to_its_target() -> None:
    catalog = build_synthetic_catalog()
    for case in C3_RETEST_AUTOMATION_CASES:
        matches = filter_catalog(
            catalog,
            module_id=case.module_id,
            dimension=case.dimension,
            query=case.query,
            focus=case.focus,
            population=case.population,
            context=case.context,
            period=case.period,
        )
        assert [row.indicator_id for row in matches] == [case.expected_indicator_id]


def test_c3_seven_new_tasks_run_through_improved_streamlit_navigation() -> None:
    for task in C3_RETEST_AUTOMATION_CASES:
        elapsed, found, passed = execute_task(task)

        assert found == task.expected_indicator_id
        assert elapsed <= HUMAN_TIME_LIMIT_SECONDS
        assert passed
