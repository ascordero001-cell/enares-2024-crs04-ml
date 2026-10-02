import csv
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.views.ui_redesign_real import (
    VISIBLE_TECHNICAL_CODE,
    safe_indicator_display_name,
)
from enares.stage04.report_topics import (
    EXPECTED_COUNTS,
    STANDARD_DISAGGREGATIONS,
    TOPIC_TITLES,
    TOPICS_WITHOUT_V0_DATA,
    VALID_PERIOD_LABELS,
    TopicCatalog,
    load_topic_mapping,
    resolve_assignment,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "app" / "data" / "v0_authorized_full_indicator_estimates.csv"
TOPIC_MAP = ROOT / "src" / "enares" / "stage04" / "report_topic_map.csv"


def catalog_rows() -> list[SimpleNamespace]:
    with FIXTURE.open(encoding="utf-8-sig", newline="") as handle:
        return [
            SimpleNamespace(
                indicator_id=record["indicator_id"].strip(),
                disaggregation=record["disaggregation"].strip(),
            )
            for record in csv.DictReader(handle)
        ]


def catalog() -> TopicCatalog:
    return load_topic_mapping(TOPIC_MAP, catalog_rows=catalog_rows())


def test_parent_fixture_invariants_are_unchanged() -> None:
    with FIXTURE.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 3014
    assert len({row["indicator_id"] for row in rows}) == 516
    assert len({row["release_id"] for row in rows}) == 1
    assert len({row["run_id"] for row in rows}) == 1


def test_every_v0_row_resolves_to_exactly_one_assignment() -> None:
    rows = catalog_rows()
    loaded = catalog()
    assert len(rows) == 3014
    assert len(loaded.topics) == 80
    assert {item.indicator_id for item in loaded.assignments.values()} == {
        row.indicator_id for row in rows
    }
    resolved = {
        (item.indicator_id, item.disaggregation_scope)
        for item in (resolve_assignment(loaded.assignments, row) for row in rows)
    }
    assert resolved == set(loaded.assignments)
    assert {
        item.period_label for item in loaded.assignments.values()
    } <= VALID_PERIOD_LABELS
    for topic in loaded.topics:
        assert bool(topic.technical_indicator_ids) == (
            topic.topic_id not in TOPICS_WITHOUT_V0_DATA
        )


def test_visible_topic_counts_titles_and_order_are_exact() -> None:
    topics = catalog().topics
    assert dict(Counter(topic.module_id for topic in topics)) == EXPECTED_COUNTS
    for module_id, expected_titles in TOPIC_TITLES.items():
        visible = sorted(
            (topic for topic in topics if topic.module_id == module_id),
            key=lambda topic: topic.order,
        )
        assert [topic.order for topic in visible] == list(
            range(1, EXPECTED_COUNTS[module_id] + 1)
        )
        assert [topic.title for topic in visible] == list(expected_titles)
        assert len(set(expected_titles)) == len(expected_titles)


def test_every_36_topic_is_national_only() -> None:
    module_36 = [topic for topic in catalog().topics if topic.module_id == "3.6"]
    assert len(module_36) == 10
    assert all(topic.national_only for topic in module_36)


def test_all_visible_labels_hide_technical_codes() -> None:
    loaded = catalog()
    topics = {topic.topic_id: topic for topic in loaded.topics}
    for item in loaded.assignments.values():
        topic = topics[item.topic_id]
        label = safe_indicator_display_name(
            item.indicator_id,
            presentation_module_id=topic.module_id,
            topic_title=topic.title,
            display_label_override=item.display_label_override,
        )
        assert label
        assert item.indicator_id.casefold() not in label.casefold()
        assert not VISIBLE_TECHNICAL_CODE.search(label)
    assert len({item.indicator_id for item in loaded.assignments.values()}) == 516


@pytest.mark.parametrize(
    ("indicator_id", "characterisation_topic"),
    (
        ("VP_HOGAR", "3.2.17"),
        ("VF_HOGAR", "3.2.18"),
        ("VP_EJERCIDA", "3.3.19"),
        ("VF_EJERCIDA", "3.3.20"),
        ("VS_12M", "3.4.09"),
    ),
)
def test_characterisation_rows_have_their_own_topic(
    indicator_id: str,
    characterisation_topic: str,
) -> None:
    loaded = catalog()
    for row in catalog_rows():
        if row.indicator_id != indicator_id:
            continue
        topic_id = resolve_assignment(loaded.assignments, row).topic_id
        if row.disaggregation in STANDARD_DISAGGREGATIONS:
            assert topic_id != characterisation_topic
        else:
            assert topic_id == characterisation_topic


@pytest.mark.parametrize(
    "topic_id",
    ("3.2.05", "3.3.05", "3.4.01", "3.4.02", "3.4.04", "3.4.05"),
)
def test_topics_with_two_reference_periods_keep_both_series(topic_id: str) -> None:
    periods = {
        item.period_label
        for item in catalog().assignments.values()
        if item.topic_id == topic_id
    }
    assert {"Últimos 12 meses", "Alguna vez en la vida"} <= periods


def test_before_age_12_period_is_explicit() -> None:
    periods = {
        item.period_label
        for item in catalog().assignments.values()
        if item.topic_id == "3.4.07"
    }
    assert periods == {"Antes de los 12 años"}


def test_no_populated_violence_or_help_topic_uses_not_applicable_period() -> None:
    loaded = catalog()
    assert all(
        item.module_id == "3.1"
        for item in loaded.assignments.values()
        if item.period_label == "No aplica"
    )
    assert "Período no precisado" in VALID_PERIOD_LABELS


@pytest.mark.parametrize(
    ("topic_id", "expected"),
    (
        ("3.2.01", {"Últimos 12 meses"}),
        ("3.2.07", {"Período no precisado"}),
        ("3.2.08", {"Período no precisado"}),
        ("3.2.17", {"Últimos 12 meses"}),
        ("3.3.19", {"Últimos 12 meses"}),
        ("3.5.09", {"Últimos 12 meses"}),
        ("3.5.10", {"Período no precisado"}),
        ("3.6.03", {"Últimos 12 meses"}),
        ("3.6.10", {"Últimos 12 meses", "Alguna vez en la vida", "Período no precisado"}),
    ),
)
def test_supervised_period_assignments_by_topic(topic_id: str, expected: set[str]) -> None:
    periods = {
        item.period_label
        for item in catalog().assignments.values()
        if item.topic_id == topic_id
    }
    assert periods == expected
