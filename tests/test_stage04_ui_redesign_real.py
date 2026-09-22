from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, cast

from streamlit.testing.v1 import AppTest

from app.streamlit_app import local_repositories
from app.views.ui_redesign_real import (
    filter_authorized_results,
    forest_record,
    load_authorized_results,
    numeric_card,
)
from enares.stage04.indicator_labels import (
    indicator_display_name,
    indicator_option_label,
)

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden" / "stage04_32_national"


def _app() -> AppTest:
    return AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(timeout=30)


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
    assert getattr(app.get("button_group")[0], "value", None) == "Resumen nacional"
    assert [selectbox.label for selectbox in app.selectbox] == [
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
        "Categoría",
    ]
    assert [selectbox.value for selectbox in app.selectbox] == [
        "Todos",
        "Todos",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
        "Todas",
        "Todos",
        "Todas",
        "Todos",
        "Todas",
    ]
    app.selectbox[0].set_value("3.2").run(timeout=30)
    indicator = next(box for box in app.selectbox if box.label == "Indicador")
    indicator.set_value("VF_HOGAR").run(timeout=30)
    category = next(box for box in app.selectbox if box.label == "Categoría")
    category.set_value("Total").run(timeout=30)
    metric_values = {metric.label: metric.value for metric in app.metric}
    assert metric_values["Estimación"] == "16.74 %"
    assert metric_values["Error estándar"] == "EE 0.5115"
    assert metric_values["CV"] == "3.06 %"
    assert metric_values["N no ponderado"] == "18,807"
    assert len(app.dataframe) == 1
    assert len(app.get("vega_lite_chart")) == 1
    record = app.dataframe[0].value.to_dict("records")[0]
    assert record["Indicador"] == "Violencia física en el hogar"
    assert record["Código"] == "VF_HOGAR"


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
        states=tuple({result.state for result in results}),
    )


def test_empty_state_filter_never_fabricates_a_value():
    app = _app()
    app.multiselect[0].set_value([]).run(timeout=30)
    assert not app.exception
    assert app.metric[0].value == "0"
    assert not app.dataframe
    assert not app.get("vega_lite_chart")
    assert any("No hay resultados autorizados" in info.value for info in app.info)


def test_one_visible_dimension_control_filters_an_existing_category_only():
    app = _app()
    area = next(box for box in app.selectbox if box.label == "Área")
    area.set_value("1").run(timeout=30)
    assert not app.exception
    assert "Dimensión" not in [box.label for box in app.sidebar.selectbox]
    assert set(app.dataframe[0].value["Categoría"]) == {"1"}
    assert all(
        box.disabled
        for box in app.selectbox
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


def test_every_v0_indicator_has_a_human_primary_label_and_keeps_its_code():
    fixture = ROOT / "app" / "data" / "v0_authorized_full_indicator_estimates.csv"
    with fixture.open(encoding="utf-8-sig", newline="") as handle:
        pairs = {
            (row["indicator_id"], row["module_id"]) for row in csv.DictReader(handle)
        }
    assert len(pairs) == 516
    labels_by_module: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for indicator_id, module_id in pairs:
        label = indicator_display_name(indicator_id, module_id)
        assert label
        assert label.casefold() != indicator_id.rstrip(",").casefold()
        assert "_" not in label
        assert not re.search(r"\bgrupo \d+\b", label, re.IGNORECASE)
        assert indicator_option_label(indicator_id, module_id) == (
            f"{label} — {indicator_id}"
        )
        labels_by_module[module_id][label].append(indicator_id)

    duplicates = {
        module_id: {
            label: indicator_ids
            for label, indicator_ids in module_labels.items()
            if len(indicator_ids) > 1
        }
        for module_id, module_labels in labels_by_module.items()
    }
    assert not {module: values for module, values in duplicates.items() if values}

    assert (
        indicator_display_name("recibio_ayuda_institucional_vs", "3.6")
        == "Recibió ayuda institucional ante violencia sexual"
    )
    assert indicator_display_name(
        "Agresor_VS_VIDA__AG_01", "3.4"
    ) != indicator_display_name("Prev_Agresor_VS__AG_01", "3.4")


def test_module_filter_and_view_stay_synchronized_in_both_directions():
    app = _app()
    view = cast(Any, app.get("button_group")[0])
    view.set_value("Módulo 3.2").run(timeout=30)
    module = next(box for box in app.selectbox if box.label == "Módulo")
    assert module.value == "3.2"
    assert app.query_params["view"] == ["Módulo 3.2"]

    module.set_value("3.4").run(timeout=30)
    assert cast(Any, app.get("button_group")[0]).value == "Módulo 3.4"
    assert app.query_params["view"] == ["Módulo 3.4"]
    assert any(heading.value == "Módulo 3.4" for heading in app.subheader)

    cast(Any, app.get("button_group")[0]).set_value("Módulo 3.1").run(timeout=30)
    assert next(box for box in app.selectbox if box.label == "Módulo").value == "3.1"
    assert app.query_params["view"] == ["Módulo 3.1"]


def test_forest_plot_requires_one_indicator_and_uses_unambiguous_labels():
    app = _app()
    assert not app.get("vega_lite_chart")
    assert any("Selecciona un indicador" in info.value for info in app.info)

    app.selectbox[0].set_value("3.2").run(timeout=30)
    indicator = next(box for box in app.selectbox if box.label == "Indicador")
    indicator.set_value("VF_HOGAR").run(timeout=30)
    assert len(app.get("vega_lite_chart")) == 1

    record = forest_record(_golden_result())
    assert record is not None
    assert record["label"] == "Violencia física en el hogar — Total"


def test_empty_selection_has_no_unrelated_indicator_sheet():
    app = _app()
    app.multiselect[0].set_value([]).run(timeout=30)
    visible = "\n".join(
        str(getattr(element, "value", ""))
        for group in (app.info, app.caption, app.markdown, app.subheader)
        for element in group
    )
    assert "No hay alertas ni indicador activo" in visible
    assert "Ficha del indicador activo" not in visible
