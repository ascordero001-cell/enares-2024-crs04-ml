from __future__ import annotations

import inspect
from pathlib import Path
from typing import get_type_hints

import pytest

from enares.stage04.release_lifecycle import ReleaseKey
from enares.stage04.repository import (
    BigQueryRepository,
    DemoRepository,
    IndicatorRepository,
    ReleaseNotFoundError,
    RepositoryContractError,
    RepositoryUnavailableError,
)
from enares.stage04.repository_cache import ReleaseRunCache


def test_repository_implementations_share_the_typed_query_signature() -> None:
    expected = inspect.signature(IndicatorRepository.list_estimates)
    expected_hints = get_type_hints(IndicatorRepository.list_estimates)

    for repository_type in (DemoRepository, BigQueryRepository):
        actual = inspect.signature(repository_type.list_estimates)
        assert tuple(actual.parameters) == tuple(expected.parameters)
        assert get_type_hints(repository_type.list_estimates) == expected_hints


def test_unavailable_repository_uses_safe_error_without_path(tmp_path: Path) -> None:
    private_path = tmp_path / "private-personal-location.csv"

    with pytest.raises(RepositoryUnavailableError) as captured:
        DemoRepository(private_path).list_estimates("3.2")

    assert str(private_path) not in str(captured.value)
    assert str(captured.value) == "Repository data is unavailable"


def test_contract_violation_uses_safe_error_without_row_details(
    tmp_path: Path,
) -> None:
    invalid_value = "caller-supplied-secret-marker"
    fixture = tmp_path / "invalid.csv"
    fixture.write_text(
        "module_id,synthetic\n3.2," + invalid_value + "\n",
        encoding="utf-8",
    )

    with pytest.raises(RepositoryContractError) as captured:
        DemoRepository(fixture).list_estimates("3.2")

    assert invalid_value not in str(captured.value)
    assert str(fixture) not in str(captured.value)
    assert str(captured.value) == "Repository data violates the aggregate contract"


def test_missing_release_uses_safe_error_without_identifiers() -> None:
    missing = ReleaseKey("private-release", "private-run")

    with pytest.raises(ReleaseNotFoundError) as captured:
        ReleaseRunCache().get(missing)

    assert missing.release_id not in str(captured.value)
    assert missing.run_id not in str(captured.value)
    assert str(captured.value) == "Requested release run is unavailable"


def test_bigquery_placeholder_reports_unavailable_without_cloud_details() -> None:
    with pytest.raises(RepositoryUnavailableError) as captured:
        BigQueryRepository().list_estimates("3.2")

    message = str(captured.value)
    assert message == "Repository data is unavailable"
    assert "project" not in message.lower()
    assert "dataset" not in message.lower()
