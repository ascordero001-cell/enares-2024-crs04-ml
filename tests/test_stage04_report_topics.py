"""Regression gates for the supervisor-approved 80 report topic names."""

from __future__ import annotations

from collections import Counter

from enares.stage04.report_topics import MODULE_NAMES, REPORT_TOPICS, TOPIC_TITLES

EXPECTED_COUNTS = {"3.1": 11, "3.2": 18, "3.3": 20, "3.4": 9, "3.5": 12, "3.6": 10}


def test_exact_authorized_topic_counts_and_modules() -> None:
    assert MODULE_NAMES == {
        "3.1": "Percepciones",
        "3.2": "Violencia en el hogar",
        "3.3": "Violencia en el entorno escolar",
        "3.4": "Violencia sexual",
        "3.5": "Acumulación de violencias",
        "3.6": "Ayuda y respuesta",
    }
    assert set(TOPIC_TITLES) == set(EXPECTED_COUNTS)
    assert Counter(topic.module_id for topic in REPORT_TOPICS) == EXPECTED_COUNTS
    assert len(REPORT_TOPICS) == 80
    assert len({topic.topic_id for topic in REPORT_TOPICS}) == 80
    assert all(
        topic.title.strip() and topic.title.endswith(".") for topic in REPORT_TOPICS
    )


def test_retired_module_36_topics_are_absent() -> None:
    assert {topic.number for topic in REPORT_TOPICS if topic.module_id == "3.6"} == set(
        range(1, 11)
    )
