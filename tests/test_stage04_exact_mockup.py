"""State, visual asset, and protected-value gates for the exact mockup."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, cast

import pytest
from streamlit.testing.v1 import AppTest

from app.streamlit_app import local_repositories
from app.ui_redesign_app import _module_summaries, _period_suffix
from app.views.ui_redesign_real import (
    AuthorizedRedesignResult,
    load_authorized_results,
    protected_export_row,
    safe_metadata_text,
    visible_table_record,
)
from enares.stage04.report_topics import (
    EXPECTED_COUNTS,
    load_topic_mapping,
    resolve_assignment,
    topic_by_id,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("module_id", EXPECTED_COUNTS)
def test_direct_module_link_initializes_one_navigation_state(module_id: str) -> None:
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py"))
    app.query_params["view"] = f"Módulo {module_id}"
    app.query_params["topic"] = f"{module_id}.01"
    app.run(timeout=30)
    assert not app.exception
    assert app.session_state["active_module_id"] == module_id
    assert app.session_state["active_report_topic_id"] == f"{module_id}.01"
    assert len(app.selectbox) == 9


def test_foreign_topic_in_url_falls_back_within_requested_module() -> None:
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py"))
    app.query_params["view"] = "Módulo 3.3"
    app.query_params["topic"] = "3.1.01"
    app.run(timeout=30)
    assert not app.exception
    assert app.session_state["active_report_topic_id"] == "3.3.01"


def test_native_navigation_has_one_visible_control_per_module_and_topic() -> None:
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(timeout=30)
    module_buttons = [
        button for button in app.button if (button.key or "").startswith("stage04_module_")
    ]
    assert len(module_buttons) == 6
    assert len(app.get("button_group")) == 2  # tabs and the visible topic selector
    assert "stage04_topic_fast_nav" not in app.session_state
    module_buttons[1].click().run(timeout=30)
    assert app.session_state["active_module_id"] == "3.2"
    assert app.session_state["active_report_topic_id"] == "3.2.01"
    assert app.query_params["view"] == ["Módulo 3.2"]
    assert app.query_params["topic"] == ["3.2.01"]
    assert len(app.get("button_group")) == 2
    cast(Any, app.get("button_group")[1]).set_value("3.2.03").run(timeout=30)
    assert app.session_state["active_report_topic_id"] == "3.2.03"
    assert app.query_params["topic"] == ["3.2.03"]


def test_versioned_mockup_css_keeps_verified_source_and_geometry() -> None:
    css = (ROOT / "app/assets/stage04_mockup.css").read_text(encoding="utf-8")
    assert (
        "source_sha256=AE6D141A40497D8FB55E4FCF924726BBD1E65CF6321B4B341747725C0FA304CB"
        in css
    )
    for token in (
        "--paper:#F1F4F9",
        "--accent:#0E7C6B",
        "max-width:1600px!important",
        "grid-template-columns:minmax(180px,210px) minmax(55%,1fr) minmax(190px,220px)",
        ".stripcard",
        ".banner",
        ".table-wrap",
    ):
        assert token in css


def test_period_suffix_is_visible_without_rewriting_catalog_titles() -> None:
    assert _period_suffix("No aplica") == ""
    assert _period_suffix("Últimos 12 meses") == " (últimos 12 meses)"
    assert _period_suffix("Alguna vez en la vida") == " (alguna vez en la vida)"
    assert _period_suffix("Período no precisado") == " (período no precisado)"
    repository, _ = local_repositories()
    results = load_authorized_results(repository)
    catalog = load_topic_mapping(
        ROOT / "src/enares/stage04/report_topic_map.csv",
        catalog_rows=[result.row for result in results],
    )
    summaries = _module_summaries(results, catalog.topics, catalog.assignments)
    assert len(summaries) == 6
    assert summaries[0]["period_suffix"] == ""
    assert all(
        row["period_suffix"] == " (últimos 12 meses)" for row in summaries[1:]
    )
    assert all("(" not in row["indicator"] for row in summaries)


def test_suppressed_sentinel_cannot_reach_table_or_export() -> None:
    repository, _ = local_repositories()
    results = load_authorized_results(repository)
    original = next(
        result
        for result in results
        if result.row.indicator_id == "justifica_castigo_parental"
        and result.row.disaggregation == "Nacional"
    )
    suppressed = AuthorizedRedesignResult(
        row=replace(
            original.row,
            estimate=99.9,
            standard_error=99.9,
            ci95_lower=99.9,
            ci95_upper=99.9,
            cv=0.999,
            n_unweighted=1,
            suppress_flag=True,
        ),
        state="SUPPRESSED",
    )
    catalog = load_topic_mapping(
        ROOT / "src/enares/stage04/report_topic_map.csv",
        catalog_rows=[result.row for result in results],
    )
    item = resolve_assignment(catalog.assignments, suppressed.row)
    topic = topic_by_id(catalog.topics)[item.topic_id]
    record = visible_table_record(suppressed, topic=topic, topic_assignment=item)
    assert record["Estimación"] == "—"
    assert record["IC95%"] == "—"
    assert record["CV"] == "—"
    assert record["N"] == "—"
    protected = protected_export_row(suppressed)
    for name in (
        "estimate",
        "standard_error",
        "ci95_lower",
        "ci95_upper",
        "cv",
        "n_unweighted",
    ):
        assert getattr(protected, name) is None


def test_every_v0_universe_and_denominator_hides_technical_codes() -> None:
    repository, _ = local_repositories()
    for result in load_authorized_results(repository):
        for source in (result.row.universe, result.row.denominator):
            visible = safe_metadata_text(source)
            assert "_" not in visible
            assert "C3P302" not in visible
