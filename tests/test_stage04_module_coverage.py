from dataclasses import replace
import hashlib
import inspect
import json
from pathlib import Path
import tomllib

import pytest
from streamlit.testing.v1 import AppTest

from app.config import FUTURE_DIMENSIONS, MODULES, NAVIGATION, get_module
from app.streamlit_app import local_repositories
from app.views.stage04_dashboard import EXPORT_ENABLED, build_numeric_card, filter_estimates
from enares.stage04.repository import (
    AuthorizedAggregateRepository,
    BigQueryRepository,
    IndicatorRepository,
)
import enares.stage04.modules as module_registry
from enares.stage04.modules import (
    AUTHORIZED_GOLDEN,
    LOCAL_COVERAGE_RUN_ID,
    PENDING_QUALITY_SUPPRESSION,
)
from enares.stage04.validation import validate_estimates


ROOT = Path(__file__).resolve().parents[1]
V0_FIXTURE = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.csv"
V0_MANIFEST = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.manifest.json"
STREAMLIT_CONFIG = ROOT / ".streamlit" / "config.toml"


def _run_application() -> AppTest:
    return AppTest.from_file(str(ROOT / "app" / "streamlit_app.py")).run(timeout=15)


def _visible_text(app: AppTest) -> str:
    groups = (
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
    for group in groups:
        for element in group:
            values.extend(
                (str(getattr(element, "value", "")), str(getattr(element, "label", "")))
            )
    return "\n".join(values)


class _StaticRepository(IndicatorRepository):
    def __init__(self, rows):
        self.rows = list(rows)

    def list_estimates(self, module_id: str):
        return [row for row in self.rows if row.module_id == module_id]


def test_registry_contains_every_module_once_in_required_order():
    assert tuple(module.module_id for module in MODULES) == (
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "3.5",
        "3.6",
    )
    assert tuple(module.order for module in MODULES) == (1, 2, 3, 4, 5, 6)
    assert len({module.indicator_ids for module in MODULES}) == 6


def test_module_36_is_help_seeking_and_navigation_is_registry_driven():
    assert get_module("3.6").label == "Búsqueda de ayuda"
    assert tuple(module.page_label for module in MODULES) == NAVIGATION[1:7]


def test_nine_dimensions_are_configured_in_required_order():
    assert FUTURE_DIMENSIONS == (
        "Nacional",
        "Sexo",
        "Área",
        "Área × sexo",
        "Idioma del hogar",
        "Discapacidad",
        "Etnicidad",
        "Tipo de hogar",
        "Departamento",
    )


def test_streamlit_theme_keeps_text_and_background_contrast_explicit():
    config = tomllib.loads(STREAMLIT_CONFIG.read_text(encoding="utf-8"))
    assert config["theme"] == {
        "base": "light",
        "primaryColor": "#9B2342",
        "backgroundColor": "#F5F7F4",
        "secondaryBackgroundColor": "#E3ECE7",
        "textColor": "#17251F",
        "font": "sans serif",
    }


def test_registry_makes_data_authorization_explicit_and_fail_closed():
    assert LOCAL_COVERAGE_RUN_ID == "sprint042-corte2-local-coverage-001"
    assert get_module("3.2").data_state == AUTHORIZED_GOLDEN
    assert get_module("3.2").authorized_dimensions == ("Nacional",)
    for module in MODULES:
        if module.module_id == "3.2":
            continue
        assert module.data_state == PENDING_QUALITY_SUPPRESSION
        assert module.authorized_dimensions == ()


def test_valid_non_synthetic_31_national_row_is_rejected_without_authorization():
    authorized, _ = local_repositories()
    golden = authorized.list_estimates("3.2")[0]
    pending = replace(
        golden,
        module_id="3.1",
        indicator_id="justifica_castigo_parental",
        indicator_name="Justificación del castigo parental",
    )
    with pytest.raises(ValueError, match="not authorized"):
        validate_estimates([pending])
    with pytest.raises(ValueError, match="not authorized"):
        filter_estimates(_StaticRepository([pending]), "3.1", "Nacional", "Total")


def test_valid_non_synthetic_32_sex_row_is_rejected_when_only_national_is_authorized():
    authorized, _ = local_repositories()
    pending = replace(
        authorized.list_estimates("3.2")[0],
        disaggregation="Sexo",
        category="Mujer",
    )
    with pytest.raises(ValueError, match="not authorized"):
        validate_estimates([pending])


def test_expanding_available_dimensions_does_not_expand_authorization(monkeypatch):
    authorized, _ = local_repositories()
    golden = authorized.list_estimates("3.2")[0]
    current = get_module("3.1")
    monkeypatch.setitem(
        module_registry.MODULE_BY_ID,
        "3.1",
        replace(current, available_dimensions=(*current.available_dimensions, "Técnica")),
    )
    pending = replace(
        golden,
        module_id="3.1",
        indicator_id="justifica_castigo_parental",
        disaggregation="Técnica",
    )
    with pytest.raises(ValueError, match="not authorized"):
        validate_estimates([pending])


def test_32_national_golden_still_builds_numeric_card():
    authorized, _ = local_repositories()
    card = build_numeric_card(filter_estimates(authorized, "3.2", "Nacional", "Total")[0])
    assert card["indicator_id"] == "VF_HOGAR"
    assert card["n_text"] == "N no ponderado: 18,807"


def test_modules_with_national_only_source_do_not_advertise_other_dimensions():
    assert get_module("3.3").available_dimensions == ("Nacional",)
    assert get_module("3.4").available_dimensions == ("Nacional",)
    assert get_module("3.6").available_dimensions == ("Nacional",)


def test_real_fixture_coverage_is_distinguished_from_configuration():
    authorized, _ = local_repositories()
    expected = {
        "3.1": set(),
        "3.2": {"Nacional"},
        "3.3": set(),
        "3.4": set(),
        "3.5": set(),
        "3.6": set(),
    }
    for module_id, dimensions in expected.items():
        rows = authorized.list_estimates(module_id)
        if rows:
            validate_estimates(rows)
        assert {row.disaggregation for row in rows} == dimensions


@pytest.mark.parametrize("module", MODULES, ids=lambda module: module.module_id)
def test_apptest_navigates_every_module_without_inventing_authorization(module):
    app = _run_application()
    app.sidebar.radio[0].set_value(module.page_label).run(timeout=15)
    visible = _visible_text(app)
    assert not app.exception
    assert module.full_label in visible
    assert f"Estado de datos: {module.data_state}" in visible
    if module.module_id != "3.2":
        assert "sin datos autorizados" in visible
        assert not app.metric
        return
    assert module.indicator_ids[0] in visible
    assert {metric.label for metric in app.metric} == {
        "Estimación",
        "Error estándar",
        "CV",
        "N no ponderado",
    }


def test_apptest_absent_combination_is_no_data_without_numbers():
    app = _run_application()
    app.sidebar.radio[0].set_value(get_module("3.1").page_label).run(timeout=15)
    app.sidebar.selectbox[0].set_value("Sexo").run(timeout=15)
    visible = _visible_text(app)
    assert not app.exception
    assert "sin datos autorizados para 3.1" in visible
    assert "No se fabrican resultados" in visible
    assert not app.metric


def test_apptest_pending_module_stops_before_repository_and_category_selector(monkeypatch):
    calls = []
    original = AuthorizedAggregateRepository.list_estimates

    def record_calls(self, module_id):
        calls.append(module_id)
        return original(self, module_id)

    monkeypatch.setattr(AuthorizedAggregateRepository, "list_estimates", record_calls)
    app = _run_application()
    app.sidebar.radio[0].set_value(get_module("3.1").page_label).run(timeout=15)
    visible = _visible_text(app)
    assert not app.exception
    assert "El gate de calidad y supresión está pendiente" in visible
    assert "sin datos autorizados" in visible
    assert set(calls) == {"3.2"}
    assert not app.metric
    assert not app.table
    assert len(app.selectbox) == 1


def test_apptest_demo_synthetic_keeps_three_textual_states():
    app = _run_application()
    app.sidebar.radio[0].set_value(get_module("3.2").page_label).run(timeout=15)
    app.radio[0].set_value("Demo sintético").run(timeout=15)
    visible = _visible_text(app)
    assert not app.exception
    assert all(state in visible for state in ("Candidato", "Referencia", "Suprimido"))
    assert visible.count("DEMO SINTÉTICO") == 3


def test_invalid_row_error_is_generic_and_does_not_expose_internal_content(monkeypatch):
    internal_marker = "<INTERNAL_STORAGE_MARKER>"
    authorized, _ = local_repositories()
    invalid = replace(authorized.list_estimates("3.2")[0], release_id=internal_marker)

    def invalid_rows(self, module_id):
        return [invalid] if module_id == "3.2" else []

    monkeypatch.setattr(AuthorizedAggregateRepository, "list_estimates", invalid_rows)
    app = _run_application()
    visible = _visible_text(app)
    assert "Los resultados no superaron la validación estadística" in visible
    assert internal_marker not in visible
    assert not app.metric


def test_authorized_filters_return_only_existing_categories():
    authorized, _ = local_repositories()
    assert filter_estimates(authorized, "3.2", "Sexo", "1") == []
    assert filter_estimates(authorized, "3.2", "Sexo", "categoría ausente") == []
    assert filter_estimates(authorized, "3.5", "Departamento", "Amazonas") == []


def test_fixture_manifest_hash_count_and_sources_match():
    manifest = json.loads(V0_MANIFEST.read_text(encoding="utf-8"))
    assert hashlib.sha256(V0_FIXTURE.read_bytes()).hexdigest() == manifest["sha256"]
    assert len(V0_FIXTURE.read_text(encoding="utf-8").splitlines()) - 1 == manifest["row_count"]
    assert manifest["source_hash"] == "15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4"
    assert manifest["sha256"] == "43f689ba9a54fb98eb3af821c76133a3ff5882abfced64dd87f0c922c3e4465e"
    assert "drive.google.com" not in V0_MANIFEST.read_text(encoding="utf-8").lower()


def test_validation_rejects_mixed_releases_and_unregistered_module_indicator():
    authorized, _ = local_repositories()
    row = authorized.list_estimates("3.2")[0]
    rows = [row, replace(row, category="synthetic-test-category")]
    with pytest.raises(ValueError, match="mix releases"):
        validate_estimates([rows[0], replace(rows[1], release_id="another-release")])
    with pytest.raises(ValueError, match="not registered"):
        validate_estimates([replace(rows[0], indicator_id="UNREGISTERED")])


def test_validation_rejects_invalid_release_and_run_ids():
    authorized, _ = local_repositories()
    row = authorized.list_estimates("3.2")[0]
    with pytest.raises(ValueError, match="release_id"):
        validate_estimates([replace(row, release_id="")])
    with pytest.raises(ValueError, match="run_id"):
        validate_estimates([replace(row, run_id="contains spaces")])


def test_ui_uses_one_generic_module_renderer_and_keeps_cloud_blocked():
    import app.streamlit_app as entrypoint

    source = inspect.getsource(entrypoint)
    assert "module_for_page(page)" in source
    assert "_module_31" not in source
    assert "_module_36" not in source
    assert EXPORT_ENABLED is False
    with pytest.raises(RuntimeError, match="BLOCKED_BY_CLOUD_GATE"):
        BigQueryRepository().list_estimates("3.6")
