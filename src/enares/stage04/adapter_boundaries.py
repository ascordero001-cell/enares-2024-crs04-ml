"""Review boundary between synthetic tests and institutional aggregates.

The institutional adapter is intentionally disconnected.  Its first aggregate
cannot be adapted until the separation recorded here receives supervisory
review.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .candidate_adapter import CandidateAggregate, CandidateScope, adapt_candidate_row


class AdapterSeparationReviewRequired(RuntimeError):
    """Raised while the institutional adapter remains at the review checkpoint."""


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
    connection_state="REVIEW_REQUIRED_BEFORE_FIRST_AGGREGATE",
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
    """Non-connected skeleton for real, manifest-bound institutional aggregates."""

    identity = INSTITUTIONAL_ADAPTER

    @staticmethod
    def assert_source_boundary(raw: Mapping[str, object]) -> None:
        if raw.get("synthetic") is not False:
            raise ValueError("Institutional adapter requires explicit synthetic=false")

    def adapt(self, raw: Mapping[str, object], scope: CandidateScope) -> CandidateAggregate:
        self.assert_source_boundary(raw)
        raise AdapterSeparationReviewRequired(
            "Institutional adapter is disconnected pending supervisory separation review"
        )
