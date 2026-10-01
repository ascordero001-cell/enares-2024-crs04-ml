from types import SimpleNamespace
from typing import cast

import pytest

from app.views.ui_redesign_real import (
    AuthorizedRedesignResult,
    ModuleIsolationError,
    enforce_module_isolation,
)
from enares.stage04.report_topics import EXPECTED_COUNTS, TOPIC_TITLES, TopicAssignment

MODULE_IDS = tuple(EXPECTED_COUNTS)


def fake_result(indicator_id: str, source_module_id: str) -> AuthorizedRedesignResult:
    return cast(
        AuthorizedRedesignResult,
        SimpleNamespace(
            row=SimpleNamespace(
                indicator_id=indicator_id,
                module_id=source_module_id,
                disaggregation="Nacional",
            )
        ),
    )


def fake_assignment(module_id: str, indicator_id: str) -> TopicAssignment:
    return TopicAssignment(
        module_id=module_id,
        topic_id=f"{module_id}.01",
        indicator_id=indicator_id,
        disaggregation_scope="ESTANDAR",
        period_label="No aplica",
        series_label="",
        display_label_override="",
    )


def test_visible_topic_counts_are_exact() -> None:
    assert {
        module: len(titles) for module, titles in TOPIC_TITLES.items()
    } == EXPECTED_COUNTS
    assert sum(EXPECTED_COUNTS.values()) == 80


@pytest.mark.parametrize("active_module", MODULE_IDS)
def test_each_module_accepts_only_its_own_rows(active_module: str) -> None:
    rows = [fake_result("indicator-a", "source-metadata-can-differ")]
    assignment = {
        ("indicator-a", "ESTANDAR"): fake_assignment(active_module, "indicator-a")
    }
    assert (
        enforce_module_isolation(
            rows,
            active_module_id=active_module,
            assignment=assignment,
        )
        == rows
    )


@pytest.mark.parametrize("active_module", MODULE_IDS)
def test_each_module_rejects_every_foreign_module(active_module: str) -> None:
    for foreign_module in MODULE_IDS:
        if foreign_module == active_module:
            continue
        own = fake_result("indicator-own", active_module)
        foreign = fake_result("indicator-foreign", active_module)
        assignment = {
            ("indicator-own", "ESTANDAR"): fake_assignment(
                active_module, "indicator-own"
            ),
            ("indicator-foreign", "ESTANDAR"): fake_assignment(
                foreign_module, "indicator-foreign"
            ),
        }
        with pytest.raises(ModuleIsolationError):
            enforce_module_isolation(
                [own, foreign],
                active_module_id=active_module,
                assignment=assignment,
            )


def test_unmapped_row_is_rejected() -> None:
    with pytest.raises(ModuleIsolationError):
        enforce_module_isolation(
            [fake_result("indicator-unmapped", "3.1")],
            active_module_id="3.1",
            assignment={},
        )
