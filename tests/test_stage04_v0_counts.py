import pytest

from enares.stage04.v0_counts import denominator_count


def test_denominator_uses_base_even_when_other_counts_differ():
    # Synthetic counts deliberately distinguish all three fields.
    assert denominator_count({"base_unw": "120", "target_unw": "30", "n_unw": "45"}) == 120


@pytest.mark.parametrize("value", [None, "", "-1", "1.5", "NaN", "inf", "unknown"])
def test_missing_or_invalid_base_never_falls_back_to_another_count(value):
    with pytest.raises(ValueError, match="base_unw"):
        denominator_count({"base_unw": value, "n_unw": "100", "target_unw": "20"})


def test_absent_base_is_rejected():
    with pytest.raises(ValueError, match="base_unw"):
        denominator_count({"n_unw": "100"})


def test_zero_base_is_preserved_without_implying_a_valid_estimate():
    assert denominator_count({"base_unw": "0"}) == 0
