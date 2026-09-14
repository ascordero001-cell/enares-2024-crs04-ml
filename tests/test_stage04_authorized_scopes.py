import pytest

from enares.stage04.adapter_boundaries import SyntheticCandidateAdapter
from enares.stage04.authorized_scopes import (
    D06_SCOPE,
    D07_SCOPE,
    D09_DOMAIN,
    D09_PAIRS,
    D09_SCOPE,
    VS_MATRIX_PAIRS,
)


def _row(scope, pair):
    dimension, category = pair
    return {
        "synthetic": True,
        "module_id": scope.module_id,
        "indicator_id": scope.indicator_id,
        "dimension": dimension,
        "category": category,
        "statistic_type": scope.output_type,
        "estimate": 12.5,
        "standard_error": 1.0,
        "ci95_lower": 10.5,
        "ci95_upper": 14.5,
        "cv": 0.08,
        "base_unw": 100,
        "target_unw": 13,
    }


@pytest.mark.parametrize("scope", (D06_SCOPE, D07_SCOPE))
def test_d06_and_d07_have_independent_adapters_and_exact_eight_pair_matrices(scope):
    assert len(scope.allowed_pairs) == 8
    assert scope.allowed_pairs == VS_MATRIX_PAIRS
    assert {dimension for dimension, _ in scope.allowed_pairs} == {"2×2", "3×3"}
    adapter = SyntheticCandidateAdapter()
    assert {
        adapter.adapt(_row(scope, pair), scope).category for pair in scope.allowed_pairs
    } == {category for _, category in scope.allowed_pairs}


def test_d06_and_d07_do_not_inherit_adapter_identity():
    assert D06_SCOPE.indicator_id != D07_SCOPE.indicator_id
    assert D06_SCOPE.adapter_id != D07_SCOPE.adapter_id


def test_d09_scope_is_closed_to_22_pairs_and_excludes_department():
    assert D09_SCOPE.allowed_pairs == D09_PAIRS
    assert len(D09_PAIRS) == 22
    assert "Departamento" not in {dimension for dimension, _ in D09_PAIRS}
    assert D09_DOMAIN == "CONS_ALGUNA = 1"
    adapter = SyntheticCandidateAdapter()
    for pair in D09_PAIRS:
        assert (
            adapter.adapt(_row(D09_SCOPE, pair), D09_SCOPE).indicator_id
            == "CONS_ATENCION_SALUD"
        )
