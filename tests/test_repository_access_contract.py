from pathlib import Path

import pytest

from enares.stage04.repository import BigQueryRepository, DemoRepository, IndicatorRepository


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "app" / "data" / "demo_indicator_estimates.csv"


def test_demo_repository_implements_expected_signature_and_preserves_quality():
    repository: IndicatorRepository = DemoRepository(FIXTURE)
    rows = repository.list_estimates("3.2")

    assert len(rows) == 3
    assert {row.quality_status for row in rows} == {
        "PUBLISHABLE_CANDIDATE",
        "REFERENCE_HIGH_CV",
        "SUPPRESSED_EXERCISE",
    }
    assert sum(row.synthetic for row in rows) == 2
    assert next(row for row in rows if row.indicator_id == "VF_HOGAR").synthetic is False
    assert all(row.engine_version == "v0_csv" for row in rows)


def test_demo_repository_exposes_no_sensitive_attributes():
    row = DemoRepository(FIXTURE).list_estimates("3.2")[0]
    forbidden = {"respondent_id", "person_id", "nna_id", "name", "birth_date", "address"}
    assert forbidden.isdisjoint(vars(row))


def test_suppressed_demo_row_contains_no_protected_statistics():
    rows = DemoRepository(FIXTURE).list_estimates("3.2")
    suppressed = next(row for row in rows if row.quality_status == "SUPPRESSED_EXERCISE")
    assert suppressed.estimate is None
    assert suppressed.standard_error is None
    assert suppressed.ci95_lower is None
    assert suppressed.ci95_upper is None
    assert suppressed.cv is None
    assert suppressed.n_unweighted is None
    assert suppressed.weighted_population is None
    assert suppressed.suppress_flag is True


def test_bigquery_repository_is_explicitly_blocked():
    with pytest.raises(RuntimeError, match="BLOCKED_BY_CLOUD_GATE"):
        BigQueryRepository().list_estimates("3.2")
