from enares.indicators.accumulation import (
    all_violence_forms,
    consequence_count,
    violence_accumulation,
)


def test_accumulation_matches_coalesce_zero_contract():
    assert violence_accumulation(1, 0, None, 1, None) == 2


def test_all_forms_requires_every_component():
    assert all_violence_forms(1, 1, 1, 1, 1) == 1
    assert all_violence_forms(1, 1, None, 1, 1) == 0


def test_consequence_count_preserves_partial_missingness():
    assert consequence_count([1, 0, 1, 0, 0, 1]) == 3
    assert consequence_count([1, 0, None, 0, 0, 1]) is None
