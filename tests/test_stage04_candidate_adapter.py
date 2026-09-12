import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from enares.stage04.candidate_adapter import (
    CandidateScope,
    adapt_candidate_row,
    candidate_view_model,
)
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
        indicator_id="SYNTHETIC_RATE",
        dimensions=frozenset({"Nacional"}),
        categories=frozenset({"Total"}),
        dictionary_type="prevalence",
        output_type="prevalence",
    )
    return replace(base, **changes)


def row(**changes):
    base = {
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


def test_target_cannot_exceed_denominator():
    with pytest.raises(ValueError, match="exceed"):
        adapt_candidate_row(row(base_unw=10, target_unw=11), scope())


def test_incomplete_statistics_are_preserved_and_never_rendered_as_metrics():
    incomplete_scope = scope(output_type="incomplete", dictionary_type="incomplete")
    adapted = adapt_candidate_row(
        row(statistic_type="incomplete", standard_error=None, ci95_lower=None, ci95_upper=None, cv=None),
        incomplete_scope,
    )
    assert adapted.standard_error is None and adapted.cv is None
    view = candidate_view_model(adapted)
    assert view["numeric_visible"] is False
    assert all(view[field] is None for field in PROTECTED_FIELDS if field in view)


@pytest.mark.parametrize("output_type", ["prevalence", "distribution", "special"])
def test_complete_statistical_families_require_all_fields(output_type):
    typed_scope = scope(dictionary_type=output_type, output_type=output_type)
    with pytest.raises(ValueError, match="all statistical fields"):
        adapt_candidate_row(row(statistic_type=output_type, cv=None), typed_scope)


def test_special_mismatch_requires_named_adapter():
    mismatched = scope(dictionary_type="special", output_type="prevalence")
    with pytest.raises(ValueError, match="explicit adapter"):
        adapt_candidate_row(row(), mismatched)
    adapted = adapt_candidate_row(row(), replace(mismatched, adapter_id="synthetic-special-v1"))
    assert adapted.statistic_type == "prevalence"


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


@pytest.mark.parametrize("flag", ["cv_flag", "n_flag", "suppress_flag"])
def test_flags_cannot_default_to_false_before_decision(flag):
    with pytest.raises(ValueError, match="pending"):
        adapt_candidate_row(row(**{flag: False}), scope())


def test_golden_32_and_manifest_hash_remain_bound():
    manifest = json.loads(V0_MANIFEST.read_text(encoding="utf-8"))
    assert hashlib.sha256(V0_CSV.read_bytes()).hexdigest() == manifest["sha256"]
    rows = AuthorizedAggregateRepository(V0_CSV, V0_MANIFEST, V0_REGISTRY).list_estimates("3.2")
    assert [(item.indicator_id, item.disaggregation, item.category) for item in rows] == [
        ("VF_HOGAR", "Nacional", "Total")
    ]


def test_suppression_nulls_every_protected_field_before_presentation():
    synthetic = {field: 1 for field in PROTECTED_FIELDS}
    synthetic.update({"cell_id": "hidden", "suppress_flag": True})
    published = apply_published_suppression([synthetic])[0]
    assert all(published[field] is None for field in PROTECTED_FIELDS)


def test_synthetic_total_margin_reconstruction_is_rejected():
    rows = [
        {"cell_id": "total", "estimate": 30, "suppress_flag": False},
        {"cell_id": "visible", "parent_total_id": "total", "estimate": 20, "suppress_flag": False},
        {"cell_id": "hidden", "parent_total_id": "total", "estimate": None, "suppress_flag": True},
    ]
    with pytest.raises(ValueError, match="reconstructed"):
        assert_no_unique_additive_reconstruction(rows)


def test_synthetic_cross_with_two_hidden_cells_is_not_uniquely_reconstructable():
    rows = [
        {"cell_id": "total", "estimate": 30, "suppress_flag": False},
        {"cell_id": "hidden-a", "parent_total_id": "total", "estimate": None, "suppress_flag": True},
        {"cell_id": "hidden-b", "parent_total_id": "total", "estimate": None, "suppress_flag": True},
    ]
    assert_no_unique_additive_reconstruction(rows)
