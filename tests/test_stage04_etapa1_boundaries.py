import inspect
from dataclasses import replace
from pathlib import Path

import pytest

from enares.stage04.adapter_boundaries import (
    INSTITUTIONAL_ADAPTER,
    SYNTHETIC_ADAPTER,
    InstitutionalAuthorizedAggregateAdapter,
    SyntheticCandidateAdapter,
)
from enares.stage04.candidate_adapter import CandidateScope
from enares.stage04.indicator_semantics import (
    C3P213_DISPLAY_LABEL,
    C3P213_DOMAIN,
    C3P213_TARGET_VALUE,
    C3P213_TARGET_VALUE_LABEL,
    D01_EXCLUDED_INDICATORS,
    D01_FEMALE_REFERENCE,
    D01_NOBODY_DENOMINATOR,
    D01_NOBODY_SERIES,
    D01_RELATIONSHIP_GROUP,
    D01_REPORTING_SUBJECT,
    D01_TASK_EXECUTION_GROUP,
    D01_TASKS,
    D01_UNIVERSE,
)
from enares.stage04.presentation import (
    PRESENTATION_SURFACES,
    dimension_label_for_surface,
    resolve_dimension_presentation,
)
from enares.stage04.repository import AuthorizedAggregateRepository, DemoRepository


def _scope() -> CandidateScope:
    return CandidateScope(
        module_id="3.1",
        indicator_id="Componentes",
        allowed_pairs=frozenset({("Tareas del hogar", "Cocinar")}),
        dictionary_type="special",
        output_type="prevalence",
        adapter_id="components-special-prevalence-v1",
    )


def _row(*, synthetic: bool) -> dict[str, object]:
    return {
        "synthetic": synthetic,
        "module_id": "3.1",
        "indicator_id": "Componentes",
        "dimension": "Tareas del hogar",
        "category": "Cocinar",
        "statistic_type": "prevalence",
        "estimate": 40.0,
        "standard_error": 1.0,
        "ci95_lower": 38.0,
        "ci95_upper": 42.0,
        "cv": 0.025,
        "base_unw": 100,
        "target_unw": 40,
    }


ROOT = Path(__file__).resolve().parents[1]
V0_CSV = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.csv"
V0_MANIFEST = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.manifest.json"
V0_REGISTRY = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"
DEMO_CSV = ROOT / "app" / "data" / "demo_indicator_estimates.csv"


def _institutional_scope() -> CandidateScope:
    return CandidateScope(
        module_id="3.2",
        indicator_id="VF_HOGAR",
        allowed_pairs=frozenset({("Nacional", "Total")}),
        dictionary_type="prevalence",
        output_type="prevalence",
        adapter_id="institutional-prevalence-v1",
    )


@pytest.mark.parametrize(
    ("source_name", "display_name", "source_code"),
    (
        ("Área y sexo", "Área × sexo", "AREA BY SEXO"),
        ("Lengua materna", "Idioma del hogar", "idiomaHogar"),
    ),
)
def test_d12_alias_is_consistent_and_preserves_source_metadata(
    source_name, display_name, source_code
):
    resolved = resolve_dimension_presentation(source_name)
    assert resolved.display_name == display_name
    assert resolved.source_name == source_name
    assert resolved.source_code == source_code
    assert {
        dimension_label_for_surface(source_name, surface)
        for surface in PRESENTATION_SURFACES
    } == {display_name}


def test_d12_rejects_unknown_source_names_and_surfaces():
    with pytest.raises(ValueError, match="Unregistered source dimension"):
        resolve_dimension_presentation("Lenguaje inventado")
    with pytest.raises(ValueError, match="Unknown presentation surface"):
        dimension_label_for_surface("Lengua materna", "hidden-html")


def test_d12_source_names_do_not_coexist_in_the_interface_dimension_selector():
    from app.config import FUTURE_DIMENSIONS

    assert "Área × sexo" in FUTURE_DIMENSIONS
    assert "Idioma del hogar" in FUTURE_DIMENSIONS
    assert "Área y sexo" not in FUTURE_DIMENSIONS
    assert "Lengua materna" not in FUTURE_DIMENSIONS


def test_d01_semantics_identify_universe_reporter_and_female_reference():
    assert "12 a 17 años" in D01_UNIVERSE
    assert "respuesta válida" in D01_UNIVERSE
    assert "adolescente entrevistada/o" in D01_REPORTING_SUBJECT
    assert D01_FEMALE_REFERENCE == ("Madre", "Hermana", "Otra mujer")
    assert tuple(item.variable for item in D01_TASKS) == tuple(
        f"tarea{number}_fem" for number in range(1, 11)
    )
    assert len({item.task for item in D01_TASKS}) == 10


def test_d01_is_presented_as_two_distinct_question_groups():
    assert tuple(item.variable for item in D01_TASK_EXECUTION_GROUP) == tuple(
        f"tarea{number}_fem" for number in range(1, 8)
    )
    assert tuple(item.variable for item in D01_RELATIONSHIP_GROUP) == tuple(
        f"tarea{number}_fem" for number in range(8, 11)
    )
    assert all(
        "la realiza principalmente" in item.display_label
        for item in D01_TASK_EXECUTION_GROUP
    )
    assert all("quien" in item.display_label for item in D01_RELATIONSHIP_GROUP)


def test_d01_nobody_addendum_is_closed_to_items_8_to_10():
    assert tuple(item.variable for item in D01_NOBODY_SERIES) == (
        "tarea8_nadie",
        "tarea9_nadie",
        "tarea10_nadie",
    )
    assert all(
        item.display_label.startswith("Porcentaje de adolescentes con quienes nadie")
        for item in D01_NOBODY_SERIES
    )
    assert D01_NOBODY_DENOMINATOR == "n_tareas_validas_8_10"
    assert D01_EXCLUDED_INDICATORS == {"predominio_femenino_tareas"}


def test_d11_records_exact_value_label_display_text_and_domain():
    assert C3P213_TARGET_VALUE == 5
    assert C3P213_TARGET_VALUE_LABEL == "No supieron cómo ayudarme"
    assert C3P213_DISPLAY_LABEL == "No recibió ayuda porque no supieron cómo ayudarle"
    assert C3P213_DOMAIN == "dom_no_recibio_hogar == 1"


def test_synthetic_adapter_keeps_the_existing_explicit_synthetic_barrier():
    adapted = SyntheticCandidateAdapter().adapt(_row(synthetic=True), _scope())
    assert adapted.adapter_id == "components-special-prevalence-v1"
    with pytest.raises(ValueError, match="synthetic=true"):
        SyntheticCandidateAdapter().adapt(_row(synthetic=False), _scope())


def test_institutional_adapter_has_distinct_identity_and_rejects_unverified_rows():
    assert SYNTHETIC_ADAPTER.adapter_id != INSTITUTIONAL_ADAPTER.adapter_id
    assert SYNTHETIC_ADAPTER.source_classification == "SYNTHETIC_TEST_ONLY"
    assert (
        INSTITUTIONAL_ADAPTER.source_classification
        == "AUTHORIZED_INSTITUTIONAL_AGGREGATE"
    )
    adapter = InstitutionalAuthorizedAggregateAdapter()
    demo = DemoRepository(DEMO_CSV).list_estimates("3.2")[0]
    with pytest.raises(ValueError, match="provenance-derived synthetic=false"):
        adapter.adapt(demo, _institutional_scope())
    with pytest.raises(ValueError, match="provenance-derived synthetic=false"):
        adapter.adapt(replace(demo, synthetic=False), _institutional_scope())


def test_institutional_adapter_accepts_only_repository_verified_local_shadow_row():
    source = AuthorizedAggregateRepository(V0_CSV, V0_MANIFEST, V0_REGISTRY)
    row = source.list_estimates("3.2")[0]
    adapted = InstitutionalAuthorizedAggregateAdapter().adapt(
        row, _institutional_scope()
    )
    assert adapted.authorization_state == "AUTHORIZED_LOCAL_SHADOW"
    assert adapted.indicator_id == "VF_HOGAR"
    assert adapted.n_unweighted == row.n_unweighted


def test_both_adapters_call_the_same_pure_statistical_rule(monkeypatch):
    from enares.stage04 import quality_rules

    calls = []
    original = quality_rules.derive_statistical_quality

    def recording_rule(**kwargs):
        calls.append(kwargs)
        return original(**kwargs)

    monkeypatch.setattr(quality_rules, "derive_statistical_quality", recording_rule)
    SyntheticCandidateAdapter().adapt(_row(synthetic=True), _scope())
    source = AuthorizedAggregateRepository(V0_CSV, V0_MANIFEST, V0_REGISTRY)
    InstitutionalAuthorizedAggregateAdapter().adapt(
        source.list_estimates("3.2")[0], _institutional_scope()
    )
    assert len(calls) == 2
    assert calls[0].keys() == calls[1].keys()


def test_application_does_not_connect_the_institutional_adapter():
    import app.streamlit_app as entrypoint

    source = inspect.getsource(entrypoint)
    assert "InstitutionalAuthorizedAggregateAdapter" not in source
    assert "adapter_boundaries" not in source
