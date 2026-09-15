import hashlib
import json
import math
from dataclasses import replace
from pathlib import Path

import pytest

from enares.stage04.candidate_adapter import (
    CV_HIGH_NOTE,
    EXACT_ZERO_CV_NOTE,
    N_SMALL_NOTE,
    CandidateScope,
    adapt_candidate_row,
    candidate_view_model,
    summarize_synthetic_health_care_domain,
)
from enares.stage04.modules import get_module
from enares.stage04.privacy import (
    PROTECTED_FIELDS,
    apply_published_suppression,
    assert_no_unique_additive_reconstruction,
)
from enares.stage04.repository import AuthorizedAggregateRepository

ROOT = Path(__file__).resolve().parents[1]
V0_CSV = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.csv"
V0_MANIFEST = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.manifest.json"
V0_REGISTRY = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"


def scope(**changes):
    base = CandidateScope(
        module_id="3.2",
        indicator_id="SYNTHETIC_RATE",
        allowed_pairs=frozenset({("Nacional", "Total")}),
        dictionary_type="prevalence",
        output_type="prevalence",
    )
    return replace(base, **changes)


def row(**changes):
    base = {
        "module_id": "3.2",
        "synthetic": True,
        "indicator_id": "SYNTHETIC_RATE",
        "dimension": "Nacional",
        "category": "Total",
        "statistic_type": "prevalence",
        "estimate": 25.0,
        "standard_error": 1.0,
        "ci95_lower": 23.0,
        "ci95_upper": 27.0,
        "cv": 0.04,
        "base_unw": 100,
        "target_unw": 25,
        "cv_flag": None,
        "n_flag": None,
        "suppress_flag": None,
    }
    return {**base, **changes}


def test_n_comes_exclusively_from_base_unw():
    adapted = adapt_candidate_row(row(base_unw=100, target_unw=25), scope())
    assert adapted.n_unweighted == 100
    assert adapted.target_unweighted == 25


@pytest.mark.parametrize("base_unw", [None, -1, 1.5, True])
def test_invalid_base_unw_is_rejected_without_target_fallback(base_unw):
    with pytest.raises(ValueError, match="base_unw"):
        adapt_candidate_row(row(base_unw=base_unw, target_unw=25), scope())


def test_candidate_adapter_rejects_non_synthetic_or_undeclared_rows():
    for synthetic in (False, None):
        with pytest.raises(ValueError, match="synthetic=true"):
            adapt_candidate_row(row(synthetic=synthetic), scope())


def test_target_cannot_exceed_denominator():
    with pytest.raises(ValueError, match="exceed"):
        adapt_candidate_row(row(base_unw=10, target_unw=11), scope())


def test_incomplete_statistics_are_preserved_and_never_rendered_as_metrics():
    incomplete_scope = scope(output_type="incomplete", dictionary_type="incomplete")
    adapted = adapt_candidate_row(
        row(
            statistic_type="incomplete",
            standard_error=None,
            ci95_lower=None,
            ci95_upper=None,
            cv=None,
        ),
        incomplete_scope,
    )
    assert adapted.standard_error is None and adapted.cv is None
    view = candidate_view_model(adapted)
    assert view["numeric_visible"] is False
    assert all(view[field] is None for field in PROTECTED_FIELDS if field in view)
    assert "target_unweighted" not in view


@pytest.mark.parametrize("output_type", ["prevalence", "distribution", "special"])
def test_complete_statistical_families_require_all_fields(output_type):
    typed_scope = scope(dictionary_type=output_type, output_type=output_type)
    with pytest.raises(ValueError, match="all statistical fields"):
        adapt_candidate_row(row(statistic_type=output_type, cv=None), typed_scope)


def test_special_mismatch_requires_named_adapter():
    mismatched = scope(dictionary_type="special", output_type="prevalence")
    with pytest.raises(ValueError, match="explicit adapter"):
        adapt_candidate_row(row(), mismatched)
    adapted = adapt_candidate_row(
        row(), replace(mismatched, adapter_id="synthetic-special-v1")
    )
    assert adapted.statistic_type == "prevalence"
    assert adapted.adapter_id == "synthetic-special-v1"
    assert adapted.authorization_state == "PENDING_NUMERIC_AUTHORIZATION"
    assert candidate_view_model(adapted)["numeric_visible"] is True


@pytest.mark.parametrize("invalid", ["", "invalid", None])
def test_unknown_scale_is_rejected_at_runtime(invalid):
    with pytest.raises(ValueError, match="Unknown scale"):
        adapt_candidate_row(row(), scope(scale=invalid))


@pytest.mark.parametrize("invalid", ["", "invalid", None])
def test_unknown_cv_unit_is_rejected_at_runtime(invalid):
    with pytest.raises(ValueError, match="Unknown CV unit"):
        adapt_candidate_row(row(), scope(cv_unit=invalid))


@pytest.mark.parametrize("field", ["dictionary_type", "output_type"])
def test_unknown_scope_statistic_type_is_rejected(field):
    with pytest.raises(ValueError, match="Unknown"):
        adapt_candidate_row(row(), scope(**{field: "invalid"}))


def test_unknown_row_statistic_type_is_rejected_even_if_scope_is_invalid_too():
    with pytest.raises(
        ValueError, match="Unknown output type|Unknown row statistic type"
    ):
        adapt_candidate_row(row(statistic_type="invalid"), scope(output_type="invalid"))


def test_unknown_row_statistic_type_is_rejected_with_a_valid_scope():
    with pytest.raises(ValueError, match="Unknown row statistic type"):
        adapt_candidate_row(row(statistic_type="invalid"), scope())


@pytest.mark.parametrize("statistic_type", ["prevalence", "distribution", "special"])
def test_each_supported_complete_type_is_accepted(statistic_type):
    adapted = adapt_candidate_row(
        row(statistic_type=statistic_type),
        scope(dictionary_type=statistic_type, output_type=statistic_type),
    )
    assert adapted.statistic_type == statistic_type


def test_supported_incomplete_type_is_accepted_with_a_real_absence():
    adapted = adapt_candidate_row(
        row(statistic_type="incomplete", cv=None),
        scope(dictionary_type="incomplete", output_type="incomplete"),
    )
    assert adapted.cv is None


@pytest.mark.parametrize(
    ("scale", "estimate", "lower", "upper"),
    [("0_1", 0.25, 0.23, 0.27), ("0_100", 25.0, 23.0, 27.0)],
)
def test_valid_scales_preserve_values(scale, estimate, lower, upper):
    adapted = adapt_candidate_row(
        row(estimate=estimate, ci95_lower=lower, ci95_upper=upper),
        scope(scale=scale),
    )
    assert (
        adapted.scale,
        adapted.estimate,
        adapted.ci95_lower,
        adapted.ci95_upper,
    ) == (
        scale,
        estimate,
        lower,
        upper,
    )


@pytest.mark.parametrize("unit", ["proportion", "percent"])
def test_valid_cv_unit_is_declared_and_preserved_without_conversion(unit):
    adapted = adapt_candidate_row(row(cv=0.25), scope(cv_unit=unit))
    assert adapted.cv == 0.25
    assert adapted.cv_unit == unit


@pytest.mark.parametrize(
    "field", ["estimate", "standard_error", "ci95_lower", "ci95_upper", "cv"]
)
@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_non_finite_statistic_is_rejected(field, value):
    with pytest.raises(ValueError, match="finite"):
        adapt_candidate_row(row(**{field: value}), scope())


@pytest.mark.parametrize(
    "field", ["estimate", "standard_error", "ci95_lower", "ci95_upper", "cv"]
)
@pytest.mark.parametrize("value", [True, "1", ""])
def test_non_numeric_or_boolean_statistic_is_rejected(field, value):
    with pytest.raises(TypeError, match="number"):
        adapt_candidate_row(row(**{field: value}), scope())


def test_present_statistic_in_incomplete_output_is_still_validated():
    with pytest.raises(ValueError, match="finite"):
        adapt_candidate_row(
            row(statistic_type="incomplete", cv=None, ci95_lower=-math.inf),
            scope(dictionary_type="incomplete", output_type="incomplete"),
        )


def test_zero_event_remains_zero_with_missing_cv_and_no_visible_metrics():
    adapted = adapt_candidate_row(
        row(
            statistic_type="incomplete",
            estimate=0,
            ci95_lower=0,
            ci95_upper=0,
            cv=None,
            target_unw=0,
        ),
        scope(
            dictionary_type="prevalence",
            output_type="incomplete",
            adapter_id="zero-event-candidate",
        ),
    )
    assert adapted.estimate == 0
    assert adapted.target_unweighted == 0
    assert adapted.cv is None
    assert candidate_view_model(adapted)["numeric_visible"] is False


def test_exact_zero_with_base_and_undefined_cv_is_a_complete_visible_output():
    adapted = adapt_candidate_row(
        row(
            estimate=0,
            standard_error=0,
            ci95_lower=0,
            ci95_upper=0,
            cv=None,
            target_unw=0,
        ),
        scope(),
    )
    view = candidate_view_model(adapted)
    assert adapted.quality_status == "EXACT_ZERO_CV_UNDEFINED"
    assert adapted.cv_flag is None
    assert adapted.quality_notes == (EXACT_ZERO_CV_NOTE,)
    assert view["numeric_visible"] is True
    assert view["estimate"] == 0


def test_invalid_present_interval_bound_is_rejected_when_another_statistic_is_missing():
    with pytest.raises(TypeError, match="ci95_lower"):
        adapt_candidate_row(
            row(
                statistic_type="incomplete",
                cv=None,
                ci95_upper=None,
                ci95_lower="invalid",
            ),
            scope(dictionary_type="incomplete", output_type="incomplete"),
        )


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"estimate": 101.0}, "scale"),
        ({"standard_error": -0.1}, "standard_error"),
        ({"cv": -0.1}, "cv"),
        ({"ci95_lower": 26.0}, "interval"),
    ],
)
def test_numeric_contract_rejects_invalid_scale_se_cv_and_interval(changes, message):
    with pytest.raises(ValueError, match=message):
        adapt_candidate_row(row(**changes), scope())


def test_reversed_finite_interval_bounds_are_rejected():
    with pytest.raises(ValueError, match="reversed"):
        adapt_candidate_row(row(ci95_lower=27.0, ci95_upper=23.0), scope())


@pytest.mark.parametrize(
    "changes",
    [
        {"indicator_id": "OTHER"},
        {"dimension": "Sexo"},
        {"category": "Mujer"},
    ],
)
def test_candidate_scope_rejects_unauthorized_indicator_dimension_and_category(changes):
    with pytest.raises(ValueError, match="scope"):
        adapt_candidate_row(row(**changes), scope())


def test_exact_dimension_category_pairs_do_not_form_a_cartesian_product():
    paired_scope = scope(
        allowed_pairs=frozenset({("Nacional", "Total"), ("Sexo", "Mujer")})
    )
    assert adapt_candidate_row(row(), paired_scope).category == "Total"
    assert (
        adapt_candidate_row(
            row(dimension="Sexo", category="Mujer"), paired_scope
        ).category
        == "Mujer"
    )
    for invalid in (
        row(dimension="Nacional", category="Mujer"),
        row(dimension="Sexo", category="Total"),
        row(dimension="Área × sexo", category="Mujer"),
        row(dimension=None, category="Total"),
        row(dimension="Nacional", category=None),
    ):
        with pytest.raises(ValueError, match="pair"):
            adapt_candidate_row(invalid, paired_scope)


def test_empty_candidate_scope_allows_no_row():
    with pytest.raises(ValueError, match="pair"):
        adapt_candidate_row(row(), scope(allowed_pairs=frozenset()))


def test_candidate_pair_does_not_change_real_authorized_dimensions():
    before = get_module("3.1").authorized_dimensions
    proposed = scope(allowed_pairs=frozenset({("Sexo", "Mujer")}))
    adapt_candidate_row(row(dimension="Sexo", category="Mujer"), proposed)
    assert get_module("3.1").authorized_dimensions == before == ("Tareas del hogar",)


@pytest.mark.parametrize("flag", ["cv_flag", "n_flag", "suppress_flag"])
def test_quality_and_confidentiality_flags_cannot_be_supplied_by_input(flag):
    with pytest.raises(ValueError, match="derived centrally"):
        adapt_candidate_row(row(**{flag: False}), scope())


@pytest.mark.parametrize("module_id", ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"])
@pytest.mark.parametrize(
    ("cv_unit", "cv", "base_unw", "expected_cv", "expected_n", "notes"),
    [
        ("proportion", 0.15, 30, False, False, ()),
        ("proportion", 0.150001, 30, True, False, (CV_HIGH_NOTE,)),
        ("percent", 15.0, 29, False, True, (N_SMALL_NOTE,)),
        ("percent", 15.0001, 29, True, True, (CV_HIGH_NOTE, N_SMALL_NOTE)),
    ],
)
def test_approved_cv_and_n_alerts_apply_without_suppression_in_all_modules(
    module_id, cv_unit, cv, base_unw, expected_cv, expected_n, notes
):
    adapted = adapt_candidate_row(
        row(module_id=module_id, cv=cv, base_unw=base_unw, target_unw=10),
        scope(module_id=module_id, cv_unit=cv_unit),
    )
    view = candidate_view_model(adapted)
    assert adapted.cv_flag is expected_cv
    assert adapted.n_flag is expected_n
    assert adapted.suppress_flag is None
    assert view["numeric_visible"] is True
    assert view["estimate"] == 25.0
    assert view["quality_notes"] == notes
    assert view["confidentiality_state"] == "PENDING_INDEPENDENT_POLICY"


def test_d09_synthetic_domain_uses_valid_responses_inside_cons_alguna_only():
    base_unw, target_unw = summarize_synthetic_health_care_domain(
        [
            {"synthetic": True, "CONS_ALGUNA": 1, "CONS_ATENCION_SALUD": 1},
            {"synthetic": True, "CONS_ALGUNA": 1, "CONS_ATENCION_SALUD": 0},
            {"synthetic": True, "CONS_ALGUNA": 1, "CONS_ATENCION_SALUD": None},
            {"synthetic": True, "CONS_ALGUNA": 0, "CONS_ATENCION_SALUD": None},
            {"synthetic": True, "CONS_ALGUNA": None, "CONS_ATENCION_SALUD": None},
        ]
    )
    assert (base_unw, target_unw) == (2, 1)


def test_d09_synthetic_domain_rejects_observed_care_outside_cons_alguna():
    with pytest.raises(ValueError, match="outside CONS_ALGUNA"):
        summarize_synthetic_health_care_domain(
            [{"synthetic": True, "CONS_ALGUNA": 0, "CONS_ATENCION_SALUD": 1}]
        )


def test_golden_32_and_manifest_hash_remain_bound():
    manifest = json.loads(V0_MANIFEST.read_text(encoding="utf-8"))
    assert hashlib.sha256(V0_CSV.read_bytes()).hexdigest() == manifest["sha256"]
    rows = AuthorizedAggregateRepository(
        V0_CSV, V0_MANIFEST, V0_REGISTRY
    ).list_estimates("3.2")
    assert [
        (item.indicator_id, item.disaggregation, item.category) for item in rows
    ] == [("VF_HOGAR", "Nacional", "Total")]


def test_suppression_nulls_every_protected_field_before_presentation():
    synthetic: dict[str, object] = {field: 1 for field in PROTECTED_FIELDS}
    synthetic.update({"cell_id": "hidden", "suppress_flag": True})
    published = apply_published_suppression([synthetic])[0]
    assert all(published[field] is None for field in PROTECTED_FIELDS)


def test_synthetic_total_margin_reconstruction_is_rejected():
    rows: list[dict[str, object]] = [
        {"cell_id": "total", "estimate": 30, "suppress_flag": False},
        {
            "cell_id": "visible",
            "parent_total_id": "total",
            "estimate": 20,
            "suppress_flag": False,
        },
        {
            "cell_id": "hidden",
            "parent_total_id": "total",
            "estimate": None,
            "suppress_flag": True,
        },
    ]
    with pytest.raises(ValueError, match="reconstructed"):
        assert_no_unique_additive_reconstruction(rows)


def test_one_total_with_two_hidden_components_has_no_unique_solution_from_that_equation():
    rows: list[dict[str, object]] = [
        {"cell_id": "total", "estimate": 30, "suppress_flag": False},
        {
            "cell_id": "hidden-a",
            "parent_total_id": "total",
            "estimate": None,
            "suppress_flag": True,
        },
        {
            "cell_id": "hidden-b",
            "parent_total_id": "total",
            "estimate": None,
            "suppress_flag": True,
        },
    ]
    assert_no_unique_additive_reconstruction(rows)
