import pytest

from enares.indicators.sexual import sexual_form_12m, vs_12m


@pytest.mark.parametrize(
    "item,recent,expected",
    [(1, 1, 1), (1, 2, 0), (2, 1, 0), (None, None, 0)],
)
def test_sexual_form_requires_occurrence_and_recent_period(item, recent, expected):
    assert sexual_form_12m(item=item, recent=recent) == expected


def test_vs_12m_aggregates_all_forms_without_changing_the_universe():
    assert vs_12m([0] * 16) == 0
    assert vs_12m([0] * 15 + [1]) == 1
