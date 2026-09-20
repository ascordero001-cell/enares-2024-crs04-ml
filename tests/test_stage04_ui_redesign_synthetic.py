from __future__ import annotations

import inspect
from pathlib import Path

from streamlit.testing.v1 import AppTest

from app.views.ui_redesign_synthetic import (
    STATE_LABELS,
    SYNTHETIC_RESULTS,
    filter_synthetic_results,
    forest_record,
    state_code,
    table_record,
)

ROOT = Path(__file__).resolve().parents[1]


def _app() -> AppTest:
    return AppTest.from_file(str(ROOT / "app" / "ui_redesign_synthetic_app.py")).run(
        timeout=15
    )


def _visible_text(app: AppTest) -> str:
    groups = (
        app.caption,
        app.error,
        app.info,
        app.markdown,
        app.metric,
        app.success,
        app.title,
        app.warning,
    )
    return "\n".join(
        str(getattr(element, "value", ""))
        for group in groups
        for element in group
    )


def test_synthetic_redesign_starts_with_native_structure():
    app = _app()
    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "Panorama",
        "Tabla",
        "Forest plot",
        "Estados",
    ]
    assert len(app.sidebar.selectbox) == 2
    assert len(app.sidebar.multiselect) == 1
    assert len(app.dataframe) == 1
    assert len(app.get("vega_lite_chart")) == 1
    assert "100 % sintética" in _visible_text(app)


def test_filters_change_visible_synthetic_rows_without_fabricating_results():
    app = _app()
    app.sidebar.selectbox[0].set_value("3.2").run(timeout=15)
    assert not app.exception
    assert app.metric[0].value == "2"
    app.sidebar.selectbox[1].set_value("Sexo").run(timeout=15)
    visible = _visible_text(app)
    assert "No hay resultados sintéticos" in visible
    assert not app.dataframe
    assert not app.get("vega_lite_chart")


def test_state_labels_are_derived_from_independent_flags():
    by_indicator = {row.indicator: state_code(row) for row in SYNTHETIC_RESULTS}
    assert by_indicator["SYN_32_B"] == "REFERENCE_HIGH_CV"
    assert by_indicator["SYN_33_A"] == "SMALL_N"
    assert by_indicator["SYN_34_A"] == "REFERENCE_HIGH_CV_AND_SMALL_N"
    assert by_indicator["SYN_35_SUPPRESSED"] == "SUPPRESSED"
    assert by_indicator["SYN_36_PENDING"] == "PENDING_AUTHORIZATION"


def test_suppressed_context_and_pending_rows_expose_no_numeric_table_values():
    hidden_states = {"SUPPRESSED", "CONTEXT_ONLY", "PENDING_AUTHORIZATION"}
    for row in SYNTHETIC_RESULTS:
        if state_code(row) not in hidden_states:
            continue
        record = table_record(row)
        assert record["Estimación (%)"] is None
        assert record["IC95 % inferior"] is None
        assert record["IC95 % superior"] is None
        assert forest_record(row) is None


def test_filter_options_cannot_escape_the_versioned_synthetic_fixture():
    rows = filter_synthetic_results(
        module_id="3.4",
        dimension="Área",
        states=tuple(STATE_LABELS),
    )
    assert [row.indicator for row in rows] == ["SYN_34_A"]
    assert filter_synthetic_results(
        module_id="9.9",
        dimension="Todas",
        states=tuple(STATE_LABELS),
    ) == []


def test_synthetic_app_does_not_import_or_read_real_repositories():
    import app.ui_redesign_synthetic_app as synthetic_app

    source = inspect.getsource(synthetic_app)
    forbidden = (
        "AuthorizedAggregateRepository",
        "BigQueryRepository",
        "configured_repositories",
        "published.v_dashboard_current",
        "unsafe_allow_html=True",
        "read_csv",
        "open(",
    )
    assert all(value not in source for value in forbidden)
