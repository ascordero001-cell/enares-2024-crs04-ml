"""Approved presentation aliases never rewrite the V0 source categories."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
import streamlit as st

from app.streamlit_app import local_repositories
from app.ui_redesign_app import _render_topic_chart
from app.views.ui_redesign_real import (
    load_authorized_results,
    rows_for_topic,
    safe_metadata_text,
)
from enares.stage04.display_taxonomy import (
    CATEGORY_LABELS,
    STANDARD_DIMENSIONS,
    assert_standard_category_coverage,
    category_sort_key,
    display_category,
    display_dimension,
)
from enares.stage04.export import build_export_records
from enares.stage04.report_topics import load_topic_mapping, topic_by_id

ROOT = Path(__file__).resolve().parents[1]


def test_every_standard_v0_category_is_labeled_and_editorially_ordered() -> None:
    with (ROOT / "app/data/v0_authorized_full_indicator_estimates.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    pairs = {(row["disaggregation"], row["category"]) for row in rows}
    assert_standard_category_coverage(pairs)
    for dimension, category in pairs:
        if dimension in CATEGORY_LABELS:
            label = display_category(dimension, category)
            assert label and label not in {"0", "1", "2", "3", "4", "5", "6", "9"}
        elif dimension not in STANDARD_DIMENSIONS and category in {"0", "1"}:
            assert display_category(dimension, category) in {"No", "Sí"}
    assert [
        display_category("Idioma del hogar", category)
        for category in sorted(
            {category for dimension, category in pairs if dimension == "Idioma del hogar"},
            key=lambda category: category_sort_key("Idioma del hogar", category),
        )
    ] == [
        "Castellano",
        "Lengua originaria de los Andes: Quechua/Aymara",
        "Lengua originaria de la Amazonía: Otra lengua nativa",
    ]
    assert display_dimension("Área") == "Ámbito de la IIEE"
    assert display_dimension("Tipo de hogar") == "Vive con padres"


def test_unknown_standard_code_fails_closed() -> None:
    with pytest.raises(ValueError, match="Unmapped V0 category"):
        display_category("Idioma del hogar", "99")


def test_export_retains_source_category_and_uses_same_display_alias() -> None:
    repository, _ = local_repositories()
    row = next(
        result.row
        for result in load_authorized_results(repository)
        if result.row.disaggregation == "Etnicidad" and result.row.category == "3"
    )
    record = build_export_records([row])[0]
    assert record["source_category"] == "3"
    assert record["category"] == display_category("Etnicidad", "3")
    assert record["source_dimension"] == "Etnicidad"
    assert record["dimension"] == "Autoidentificación étnica"
    assert record["estimate_percent"] == row.estimate


def test_mixed_universe_conditions_hide_spss_boolean_syntax() -> None:
    assert safe_metadata_text("dom_recibio_hogar == 1") == (
        "quienes recibieron ayuda por violencia en el hogar"
    )
    assert "==" not in safe_metadata_text("VP_o_VF_HOGAR == 0")
    assert safe_metadata_text("SEXO == 1") == "Hombres"


def test_department_chart_has_26_complete_labels_and_selected_block(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository, _ = local_repositories()
    results = load_authorized_results(repository)
    catalog = load_topic_mapping(
        ROOT / "src/enares/stage04/report_topic_map.csv",
        catalog_rows=[result.row for result in results],
    )
    topic = topic_by_id(catalog.topics)["3.2.01"]
    rows = rows_for_topic(
        results,
        active_module_id="3.2",
        topic=topic,
        assignment=catalog.assignments,
    )
    charts: list[tuple[list[dict[str, object]], dict[str, object]]] = []
    monkeypatch.setattr(st, "caption", lambda _text: None)
    monkeypatch.setattr(st, "html", lambda _text: None)
    monkeypatch.setattr(st, "vega_lite_chart", lambda data, spec, **_kwargs: charts.append((data, spec)))
    _render_topic_chart(
        topic,
        rows,
        catalog.assignments,
        active_dimension="Departamento",
        active_category="Callao",
    )
    assert len(charts) == 1
    records, spec = charts[0]
    assert len(records) == 26
    labels = {str(record["label"]) for record in records}
    assert {"Amazonas", "Callao", "Lima Metropolitana", "Región Lima"} <= labels
    assert not any("Departamento ·" in label for label in labels)
    assert sum(bool(record["selected"]) for record in records) == 1
    estimates = [float(str(record["estimate"])) for record in records]
    assert estimates == sorted(estimates, reverse=True)
    layers = spec["layer"]
    assert isinstance(layers, list)
    assert layers[1]["encoding"]["y"]["axis"]["labelLimit"] >= 260
