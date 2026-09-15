import inspect
from dataclasses import replace
from pathlib import Path

import pytest
import tomllib
from streamlit.testing.v1 import AppTest

from app.streamlit_app import local_repositories
from app.views.stage04_dashboard import (
    build_numeric_card,
    build_state_cards,
    filter_estimates,
    load_validated_estimates,
)
from enares.stage04.repository import IndicatorEstimate, IndicatorRepository

ROOT = Path(__file__).resolve().parents[1]
SENTINEL = "<img src=x onerror=alert(1)>"


class StaticRepository(IndicatorRepository):
    def __init__(self, rows: list[IndicatorEstimate]) -> None:
        self.rows = rows

    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        return [row for row in self.rows if row.module_id == module_id]


class ExplodingRepository(IndicatorRepository):
    def list_estimates(self, module_id: str) -> list[IndicatorEstimate]:
        raise ValueError(r"C:\Users\private\microdata.sav token=secret-value")


def valid_v0_row() -> IndicatorEstimate:
    authorized, _ = local_repositories()
    return authorized.list_estimates("3.2")[0]


def valid_suppressed_row() -> IndicatorEstimate:
    _, demo = local_repositories()
    return next(row for row in demo.list_estimates("3.2") if row.suppress_flag)


@pytest.mark.parametrize(
    "changes",
    [
        {"standard_error": -1.0},
        {"cv": -0.1},
        {"n_unweighted": -1},
        {"estimate": 101.0},
        {"ci95_lower": 20.0},
        {"source_hash": "invalid"},
        {"validation_status": "FAILED"},
        {"suppress_flag": True, "quality_status": "SUPPRESSED_EXERCISE"},
        {"quality_status": "SUPPRESSED_EXERCISE", "suppress_flag": False},
    ],
    ids=(
        "negative-se",
        "negative-cv",
        "negative-n",
        "outside-scale",
        "inconsistent-ci95",
        "invalid-source-hash",
        "failed-validation",
        "visible-suppressed-statistics",
        "inconsistent-quality-state",
    ),
)
def test_invalid_repository_rows_are_blocked_before_filtering(changes):
    repository = StaticRepository([replace(valid_v0_row(), **changes)])
    with pytest.raises(ValueError):
        filter_estimates(repository, "3.2", "Nacional", "Total")


def test_empty_catalog_is_a_valid_no_data_result():
    repository = StaticRepository([])
    assert load_validated_estimates(repository, "3.2") == []
    assert filter_estimates(repository, "3.2", "Nacional", "Total") == []


def test_valid_v0_row_builds_a_numeric_card():
    card = build_numeric_card(valid_v0_row())
    assert card["estimate_text"] == "16.74 %"
    assert card["release_id"] == "enares2024-crs04-v0-shadow-001"


def test_numeric_card_has_its_own_validation_guard():
    with pytest.raises(ValueError, match="non-negative"):
        build_numeric_card(replace(valid_v0_row(), standard_error=-1.0))


def test_numeric_card_rejects_suppressed_rows_before_formatting():
    with pytest.raises(ValueError, match="suppressed row"):
        build_numeric_card(valid_suppressed_row())


def test_state_gallery_validates_the_complete_catalog_first():
    _, demo = local_repositories()
    rows = demo.list_estimates("3.2")
    invalid = [replace(rows[0], cv=-0.1), *rows[1:]]
    with pytest.raises(ValueError, match="non-negative"):
        build_state_cards(StaticRepository(invalid))


def test_correctly_nullified_suppressed_row_builds_only_non_numeric_state():
    card = build_state_cards(StaticRepository([valid_suppressed_row()]))[0]
    assert card["protected_values_visible"] is False
    for field in (
        "estimate",
        "standard_error",
        "ci95_lower",
        "ci95_upper",
        "cv",
        "n_unweighted",
        "weighted_population",
    ):
        assert card[field] is None


def _run_application() -> AppTest:
    return AppTest.from_file(str(ROOT / "app" / "streamlit_app.py")).run(timeout=15)


def _visible_text(app: AppTest) -> str:
    element_groups = (
        app.caption,
        app.error,
        app.info,
        app.markdown,
        app.metric,
        app.subheader,
        app.text,
        app.title,
        app.warning,
    )
    values = []
    for group in element_groups:
        for element in group:
            values.append(str(getattr(element, "value", "")))
            values.append(str(getattr(element, "label", "")))
    return "\n".join(values)


def test_apptest_summary_shows_local_status_release_and_golden_statistics():
    app = _run_application()
    visible = _visible_text(app)
    assert not app.exception
    assert "DEMO/SHADOW" in visible
    assert "enares2024-crs04-v0-shadow-001" in visible
    assert "No es una publicación institucional" in visible
    assert {metric.label for metric in app.metric} == {
        "Estimación",
        "Error estándar",
        "CV",
        "N no ponderado",
    }
    assert {metric.value for metric in app.metric} == {
        "16.74 %",
        "EE 0.5115",
        "0.03055",
        "18,807",
    }
    assert "IC95 %: 15.74 %–17.75 %" in visible


def test_apptest_module_32_shows_golden_and_three_demo_states():
    app = _run_application()
    app.sidebar.radio[0].set_value("Módulo 3.2").run(timeout=15)
    visible = _visible_text(app)
    assert "16.74 %" in visible
    source = next(radio for radio in app.radio if radio.label == "Fuente local")
    source.set_value("Demo sintético").run(timeout=15)
    visible = _visible_text(app)
    assert "Candidato — revisión pendiente" in visible
    assert "Referencial — precisión limitada" in visible
    assert "CV superior al 15 %" in visible
    assert "Suprimido — confidencialidad protegida" in visible
    assert "no derivado de CV ni N" in visible
    assert "Los campos protegidos no llegan a la interfaz" in visible
    assert "weighted_population" not in visible


def test_apptest_unsupported_dimension_shows_no_data_without_a_number():
    app = _run_application()
    app.sidebar.selectbox[0].set_value("Sexo").run(timeout=15)
    visible = _visible_text(app)
    assert "Sexo: sin datos" in visible
    assert "No se fabrican resultados" in visible
    assert not app.metric
    assert "16.74 %" not in visible


def test_apptest_controls_remain_local_and_safe_export_is_available():
    app = _run_application()
    visible = _visible_text(app)
    assert "Exportación agregada: 1 fila(s)" in visible
    assert len(app.get("download_button")) == 2
    assert "Cloud: NOT_AUTHORIZED" in _visible_text(app)
    app.sidebar.radio[0].set_value("Estado del release").run(timeout=15)
    visible = _visible_text(app)
    assert "PUBLISHED: NOT_AUTHORIZED" in visible
    assert "búsqueda individual" in visible


def test_apptest_demo_does_not_offer_institutional_export():
    app = _run_application()
    app.sidebar.radio[0].set_value("Módulo 3.2").run(timeout=15)
    source = next(radio for radio in app.radio if radio.label == "Fuente local")
    source.set_value("Demo sintético").run(timeout=15)
    assert not app.get("download_button")


def test_streamlit_local_hardening_is_versioned():
    with (ROOT / ".streamlit" / "config.toml").open("rb") as handle:
        client = tomllib.load(handle)["client"]
    assert client == {
        "toolbarMode": "viewer",
        "disableDataExport": True,
        "showErrorDetails": "none",
    }


def test_apptest_escapes_repository_html_sentinel_before_display():
    def sentinel_application(row):
        import streamlit as st

        from app.views.stage04_dashboard import build_numeric_card

        card = build_numeric_card(row)
        st.text(card["category"])

    row = replace(valid_v0_row(), category=SENTINEL)
    app = AppTest.from_function(sentinel_application, args=(row,)).run(timeout=15)
    assert not app.exception
    assert app.text[0].value == "&lt;img src=x onerror=alert(1)&gt;"
    assert SENTINEL not in app.text[0].value


def test_unsafe_html_is_limited_to_static_css():
    import app.streamlit_app as entrypoint

    source = inspect.getsource(entrypoint)
    style_source = inspect.getsource(entrypoint._styles)
    assert source.count("unsafe_allow_html=True") == 1
    assert "unsafe_allow_html=True" in style_source
    assert 'st.markdown(\n        f"' not in source


def test_apptest_invalid_statistic_never_reaches_a_metric():
    def guarded_application(repository):
        from app.streamlit_app import _validated_state_gallery

        _validated_state_gallery(repository)

    invalid = StaticRepository([replace(valid_v0_row(), standard_error=-1.0)])
    app = AppTest.from_function(guarded_application, args=(invalid,)).run(timeout=15)
    assert not app.exception
    assert (
        app.error[0].value == "Los resultados no superaron la validación estadística."
    )
    assert not app.metric


def test_apptest_internal_error_exposes_no_path_token_or_file_content():
    def guarded_application(repository):
        from app.streamlit_app import _validated_state_gallery

        _validated_state_gallery(repository)

    app = AppTest.from_function(
        guarded_application,
        args=(ExplodingRepository(),),
    ).run(timeout=15)
    visible = _visible_text(app)
    assert not app.exception
    assert "Los resultados no superaron la validación estadística" in visible
    assert "C:\\Users" not in visible
    assert "microdata.sav" not in visible
    assert "secret-value" not in visible
