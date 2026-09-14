"""Separate adapters for synthetic tests and provenance-verified aggregates."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .candidate_adapter import (
    CandidateAggregate,
    CandidateScope,
    _adapt_row_after_source_boundary,
    adapt_candidate_row,
)
from .repository import IndicatorEstimate, is_verified_authorized_estimate


@dataclass(frozen=True)
class AdapterIdentity:
    name: str
    version: str
    source_classification: str
    connection_state: str

    @property
    def adapter_id(self) -> str:
        return f"{self.name}-v{self.version}"


SYNTHETIC_ADAPTER = AdapterIdentity(
    name="synthetic-candidate",
    version="1",
    source_classification="SYNTHETIC_TEST_ONLY",
    connection_state="LOCAL_TEST_ONLY",
)
INSTITUTIONAL_ADAPTER = AdapterIdentity(
    name="institutional-authorized-aggregate",
    version="1",
    source_classification="AUTHORIZED_INSTITUTIONAL_AGGREGATE",
    connection_state="PROVENANCE_GATE_REQUIRED",
)


class SyntheticCandidateAdapter:
    """Exercise candidate mappings using only explicit synthetic rows."""

    identity = SYNTHETIC_ADAPTER

    def adapt(
        self,
        raw: Mapping[str, object],
        scope: CandidateScope,
    ) -> CandidateAggregate:
        return adapt_candidate_row(raw, scope)


class InstitutionalAuthorizedAggregateAdapter:
    """Adapt only aggregates classified by AuthorizedAggregateRepository."""

    identity = INSTITUTIONAL_ADAPTER

    @staticmethod
    def assert_source_boundary(row: IndicatorEstimate) -> None:
        if not is_verified_authorized_estimate(row):
            raise ValueError(
                "Institutional adapter requires provenance-derived synthetic=false"
            )

    def adapt(
        self, row: IndicatorEstimate, scope: CandidateScope
    ) -> CandidateAggregate:
        self.assert_source_boundary(row)
        raw = {
            "module_id": row.module_id,
            "indicator_id": row.indicator_id,
            "dimension": row.disaggregation,
            "category": row.category,
            "statistic_type": scope.output_type,
            "estimate": row.estimate,
            "standard_error": row.standard_error,
            "ci95_lower": row.ci95_lower,
            "ci95_upper": row.ci95_upper,
            "cv": row.cv,
            "base_unw": row.n_unweighted,
            "target_unw": None,
        }
        return _adapt_row_after_source_boundary(
            raw,
            scope,
            authorization_state="AUTHORIZED_LOCAL_SHADOW",
        )
