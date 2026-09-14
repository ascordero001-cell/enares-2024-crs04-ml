import inspect

import pytest

from enares.stage04.adapter_boundaries import (
    INSTITUTIONAL_ADAPTER,
    SYNTHETIC_ADAPTER,
    AdapterSeparationReviewRequired,
    InstitutionalAuthorizedAggregateAdapter,
    SyntheticCandidateAdapter,
)
from enares.stage04.candidate_adapter import CandidateScope
from enares.stage04.indicator_semantics import (
    C3P213_DISPLAY_LABEL,
    C3P213_DOMAIN,
    C3P213_TARGET_VALUE,
    C3P213_TARGET_VALUE_LABEL,
    D01_FEMALE_REFERENCE,
    D01_REPORTING_SUBJECT,
    D01_TASKS,
    D01_UNIVERSE,
)
from enares.stage04.presentation import (
    PRESENTATION_SURFACES,
    dimension_label_for_surface,
    resolve_dimension_presentation,
)


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


def test_institutional_adapter_has_distinct_identity_and_rejects_synthetic_rows():
    assert SYNTHETIC_ADAPTER.adapter_id != INSTITUTIONAL_ADAPTER.adapter_id
    assert SYNTHETIC_ADAPTER.source_classification == "SYNTHETIC_TEST_ONLY"
    assert INSTITUTIONAL_ADAPTER.source_classification == "AUTHORIZED_INSTITUTIONAL_AGGREGATE"
    adapter = InstitutionalAuthorizedAggregateAdapter()
    with pytest.raises(ValueError, match="synthetic=false"):
        adapter.adapt(_row(synthetic=True), _scope())


def test_institutional_adapter_stops_before_first_real_aggregate():
    adapter = InstitutionalAuthorizedAggregateAdapter()
    with pytest.raises(AdapterSeparationReviewRequired, match="separation review"):
        adapter.adapt(_row(synthetic=False), _scope())


def test_application_does_not_connect_the_institutional_adapter():
    import app.streamlit_app as entrypoint

    source = inspect.getsource(entrypoint)
    assert "InstitutionalAuthorizedAggregateAdapter" not in source
    assert "adapter_boundaries" not in source
