import pytest

from enares.indicators.perceptions import (
    justified_any,
    recode_rejection,
    recode_yes_no,
)


@pytest.mark.parametrize("source,expected", [(1, 1), (2, 0), (None, None), (9, None)])
def test_yes_no_recode_preserves_missing(source, expected):
    assert recode_yes_no(source) == expected


@pytest.mark.parametrize("source,expected", [(1, 0), (2, 1), (None, None)])
def test_rejection_reverses_only_valid_answers(source, expected):
    assert recode_rejection(source) == expected


def test_justification_aggregate_distinguishes_zero_from_all_missing():
    assert justified_any(None, None) is None
    assert justified_any(0, None) == 0
    assert justified_any(0, 1) == 1
