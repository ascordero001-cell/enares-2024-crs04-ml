import pytest

from enares.indicators.help_seeking import (
    help_gap,
    received_help_for_victim,
    recode_yes_no,
)


@pytest.mark.parametrize("source,expected", [(1, 1), (2, 0), (3, None), (None, None)])
def test_help_search_recode_preserves_nonresponse(source, expected):
    assert recode_yes_no(source) == expected


def test_received_help_is_defined_only_in_the_victim_universe():
    assert received_help_for_victim(victim=0, response=1) is None
    assert received_help_for_victim(victim=1, response=1) == 1
    assert received_help_for_victim(victim=1, response=2) == 0
    assert received_help_for_victim(victim=1, response=3) is None


def test_help_gap_is_defined_only_after_a_valid_help_search():
    assert help_gap(searched=1, received=0) == 1
    assert help_gap(searched=1, received=1) == 0
    assert help_gap(searched=0, received=0) is None
    assert help_gap(searched=1, received=None) is None
