from __future__ import annotations

import json
from pathlib import Path

from streamlit.testing.v1 import AppTest

from app.streamlit_app import local_repositories
from app.views.ui_redesign_real import (
    filter_authorized_results,
    load_authorized_results,
    numeric_card,
)

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden" / "stage04_32_national"


def _app() -> AppTest:
    return AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(
        timeout=30
    )


def _golden_card() -> dict[str, object]:
    return json.loads(
        (GOLDEN / "expected_card_view_model.json").read_text(encoding="utf-8")
    )


def _golden_result():
    repository, _ = local_repositories()
    results = load_authorized_results(repository)
    matches = filter_authorized_results(
        results,
        module_id="3.2",
        dimension="Nacional",
        indicator_id="VF_HOGAR",
        states=("PUBLISHABLE_SHADOW",),
    )
    assert len(matches) == 1
    return matches[0]


def test_authorized_redesign_reuses_repository_and_matches_golden_card_exactly():
    card = numeric_card(_golden_result())
    assert card is not None
    expected = _golden_card()
    for field, value in expected.items():
        assert card[field] == value


def test_redesign_app_displays_the_exact_golden_values_by_default():
    app = _app()
    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "Panorama",
        "Tabla",
        "Forest plot",
        "Estados",
    ]
    assert [selectbox.label for selectbox in app.sidebar.selectbox] == [
        "Módulo",
        "Departamento",
        "Área",
        "Sexo",
        "Área × sexo",
        "Idioma del hogar",
        "Etnicidad",
        "Tipo de hogar",
        "Discapacidad",
        "Indicador",
    ]
    assert [selectbox.value for selectbox in app.sidebar.selectbox] == [
        "3.2",
        "Todos",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
        "Todas",
        "Todos",
        "Todas",
        "VF_HOGAR",
    ]
    metric_values = {metric.label: metric.value for metric in app.metric}
    assert metric_values["Estimación"] == "16.74 %"
    assert metric_values["Error estándar"] == "EE 0.5115"
    assert metric_values["CV"] == "3.06 %"
    assert metric_values["N no ponderado"] == "18,807"
    assert len(app.dataframe) == 1
    assert len(app.get("vega_lite_chart")) == 1


def test_filter_options_are_derived_from_authorized_rows_only():
    repository, _ = local_repositories()
    results = load_authorized_results(repository)
    modules = {result.row.module_id for result in results}
    assert modules == {"3.1", "3.2", "3.3", "3.4", "3.5", "3.6"}
    assert not filter_authorized_results(
        results,
        module_id="3.2",
        dimension="Distrito",
        indicator_id="VF_HOGAR",
        states=tuple(
            {
                result.state
                for result in results
            }
        ),
    )


def test_empty_state_filter_never_fabricates_a_value():
    app = _app()
    app.sidebar.multiselect[0].set_value([]).run(timeout=30)
    assert not app.exception
    assert app.metric[0].value == "0"
    assert not app.dataframe
    assert not app.get("vega_lite_chart")
    assert any("No hay resultados autorizados" in info.value for info in app.info)


def test_one_visible_dimension_control_filters_an_existing_category_only():
    app = _app()
    area = next(box for box in app.sidebar.selectbox if box.label == "Área")
    area.set_value("1").run(timeout=30)
    assert not app.exception
    assert "Dimensión" not in [box.label for box in app.sidebar.selectbox]
    assert set(app.dataframe[0].value["Categoría"]) == {"1"}
    assert all(
        box.disabled
        for box in app.sidebar.selectbox
        if box.label
        in {
            "Departamento",
            "Área",
            "Sexo",
            "Área × sexo",
            "Idioma del hogar",
            "Etnicidad",
            "Tipo de hogar",
            "Discapacidad",
        }
        and box.label != "Área"
    )
