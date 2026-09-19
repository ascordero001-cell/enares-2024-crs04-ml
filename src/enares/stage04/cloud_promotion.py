"""Protected promotion of an already reconciled Stage 04 snapshot."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from google.cloud import bigquery

from .repository import BIGQUERY_MAXIMUM_BYTES_BILLED

_IDENTITY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{2,127}")
_FIVE_GATES = {
    "technical",
    "v0_parity",
    "privacy",
    "release_consistency",
    "query_cost_cap",
}


@dataclass(frozen=True)
class PromotionDecision:
    schema_version: str
    action: str
    status: str
    reviewer: str
    scope: str
    release_id: str
    run_id: str
    source_hash: str
    reconciliation_run_url: str
    allow_public_access: bool
    allow_cutover: bool


@dataclass(frozen=True)
class PromotionEvidence:
    status: str
    release_id: str
    run_id: str
    row_count: int
    indicator_count: int
    validation_gate_count: int
    source_hash_match: bool
    fail_closed_view_applied: bool
    pointer_updated: bool
    published_view_updated: bool
    event_recorded: bool
    maximum_bytes_billed: int

    def as_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


@dataclass(frozen=True)
class PromotionResources:
    outputs_table: str
    release_registry: str
    validation_results: str
    current_release: str
    promotion_events: str
    published_view: str

    def validate(self) -> None:
        pattern = re.compile(
            r"[A-Za-z0-9][A-Za-z0-9_-]*\.[A-Za-z0-9_]+\.[A-Za-z0-9_]+"
        )
        for value in asdict(self).values():
            if not isinstance(value, str) or not pattern.fullmatch(value):
                raise ValueError("Promotion resource identity is invalid")


def load_promotion_decision(
    path: Path,
    *,
    release_id: str,
    run_id: str,
    source_hash: str,
    reconciliation_run_url: str,
) -> PromotionDecision:
    """Require a versioned, exact and non-expansive supervisory decision."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    decision = PromotionDecision(**payload)
    if (
        decision.schema_version != "stage04-promotion-decision-v1"
        or decision.action != "APPROVE_AUTHENTICATED_SHADOW_PROMOTION"
        or decision.status != "APPROVED"
        or decision.reviewer != "ritaricaldi-cpu"
        or decision.scope != "CONTROLLED_SHADOW"
        or decision.release_id != release_id
        or decision.run_id != run_id
        or decision.source_hash.lower() != source_hash.lower()
        or decision.reconciliation_run_url != reconciliation_run_url
        or decision.allow_public_access
        or decision.allow_cutover
    ):
        raise ValueError("Promotion decision does not match the reconciled snapshot")
    if not _IDENTITY.fullmatch(release_id) or not _IDENTITY.fullmatch(run_id):
        raise ValueError("Promotion identity is invalid")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", source_hash):
        raise ValueError("Promotion source hash is invalid")
    if not reconciliation_run_url.startswith(
        "https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/runs/"
    ):
        raise ValueError("Reconciliation reference is invalid")
    return decision


def _config(*parameters: bigquery.ScalarQueryParameter) -> bigquery.QueryJobConfig:
    return bigquery.QueryJobConfig(
        maximum_bytes_billed=BIGQUERY_MAXIMUM_BYTES_BILLED,
        use_query_cache=False,
        query_parameters=list(parameters),
    )


def _rows(client: Any, query: str, config: bigquery.QueryJobConfig) -> list[Any]:
    return list(client.query(query, job_config=config).result())


def _literal(value: str) -> str:
    if not _IDENTITY.fullmatch(value):
        raise ValueError("Promotion identity is invalid")
    return value


def promote_reconciled_release(
    *,
    client: Any,
    decision: PromotionDecision,
    resources: PromotionResources,
    decision_reference: str,
) -> PromotionEvidence:
    """Promote an exact approved snapshot, leaving the view empty on partial failure."""

    resources.validate()
    release_id = _literal(decision.release_id)
    run_id = _literal(decision.run_id)
    common = (
        bigquery.ScalarQueryParameter("release_id", "STRING", release_id),
        bigquery.ScalarQueryParameter("run_id", "STRING", run_id),
    )
    summary = _rows(
        client,
        f"""
        SELECT COUNT(*) AS row_count,
               COUNT(DISTINCT indicator_id) AS indicator_count,
               COUNTIF(source_hash != @source_hash) AS source_hash_mismatches,
               COUNTIF(validation_status != 'APPROVED') AS invalid_rows
        FROM `{resources.outputs_table}`
        WHERE release_id = @release_id AND run_id = @run_id
        """,
        _config(
            *common,
            bigquery.ScalarQueryParameter(
                "source_hash", "STRING", decision.source_hash.upper()
            ),
        ),
    )[0]
    if (
        int(summary["row_count"]) != 3014
        or int(summary["indicator_count"]) != 516
        or int(summary["source_hash_mismatches"]) != 0
        or int(summary["invalid_rows"]) != 0
    ):
        raise ValueError("Reconciled output no longer matches the approved snapshot")

    registry = _rows(
        client,
        f"""
        SELECT COUNT(*) AS approved_count
        FROM `{resources.release_registry}`
        WHERE release_id = @release_id AND run_id = @run_id
          AND validation_status = 'APPROVED' AND approval_reference IS NOT NULL
        """,
        _config(*common),
    )[0]
    if int(registry["approved_count"]) != 1:
        raise ValueError("Release registry does not contain one approved snapshot")

    gates = _rows(
        client,
        f"""
        SELECT validation_name, validation_status
        FROM `{resources.validation_results}`
        WHERE release_id = @release_id AND run_id = @run_id
        """,
        _config(*common),
    )
    observed_gates = {
        str(row["validation_name"])
        for row in gates
        if str(row["validation_status"]) == "PASS"
    }
    if observed_gates != _FIVE_GATES or len(gates) != len(_FIVE_GATES):
        raise ValueError("Promotion gates are incomplete or inconsistent")

    projection = """
      release_id, run_id, source_version, source_hash, git_commit_sha,
      container_image_digest, dataform_release, engine_version, scale,
      indicator_id, indicator_name, module_id, disaggregation, category,
      IF(suppress_flag, NULL, estimate) AS estimate,
      IF(suppress_flag, NULL, standard_error) AS standard_error,
      IF(suppress_flag, NULL, ci95_lower) AS ci95_lower,
      IF(suppress_flag, NULL, ci95_upper) AS ci95_upper,
      IF(suppress_flag, NULL, cv) AS cv,
      IF(suppress_flag, NULL, n_unweighted) AS n_unweighted,
      IF(suppress_flag, NULL, weighted_population) AS weighted_population,
      cv_flag, n_flag, suppress_flag, quality_note, validation_status,
      created_at, universe, denominator, quality_status
    """
    _rows(
        client,
        f"CREATE OR REPLACE VIEW `{resources.published_view}` AS "
        f"SELECT {projection} FROM `{resources.outputs_table}` WHERE FALSE",
        _config(),
    )
    _rows(
        client,
        f"""
        DECLARE previous_release STRING;
        DECLARE previous_run STRING;
        DECLARE current_release_id STRING;
        DECLARE current_run_id STRING;
        SET (previous_release, previous_run) = (
          SELECT AS STRUCT ANY_VALUE(previous_release_id), ANY_VALUE(previous_run_id)
          FROM `{resources.current_release}` WHERE singleton = TRUE
        );
        SET (current_release_id, current_run_id) = (
          SELECT AS STRUCT ANY_VALUE(release_id), ANY_VALUE(run_id)
          FROM `{resources.current_release}` WHERE singleton = TRUE
        );
        IF current_release_id IS DISTINCT FROM @release_id
           OR current_run_id IS DISTINCT FROM @run_id THEN
          SET previous_release = current_release_id;
          SET previous_run = current_run_id;
          BEGIN TRANSACTION;
            DELETE FROM `{resources.current_release}` WHERE TRUE;
            INSERT INTO `{resources.current_release}`
              (singleton, release_id, run_id, previous_release_id, previous_run_id,
               promoted_at, promoted_by, reason)
            VALUES
              (TRUE, @release_id, @run_id, previous_release, previous_run,
               CURRENT_TIMESTAMP(), 'github-actions-protected',
               'approved automated authenticated shadow promotion');
          COMMIT TRANSACTION;
        END IF;
        """,
        _config(*common),
    )
    _rows(
        client,
        f"""
        CREATE OR REPLACE VIEW `{resources.published_view}` AS
        SELECT {projection}
        FROM `{resources.outputs_table}`
        WHERE release_id = "{release_id}" AND run_id = "{run_id}"
          AND validation_status = "APPROVED"
        """,
        _config(),
    )

    event_id = hashlib.sha256(
        f"{release_id}\n{run_id}\n{decision_reference}".encode()
    ).hexdigest()
    _rows(
        client,
        f"""
        MERGE `{resources.promotion_events}` AS target
        USING (SELECT @event_id AS event_id) AS source
        ON target.event_id = source.event_id
        WHEN NOT MATCHED THEN INSERT
          (event_id, event_type, release_id, run_id, previous_release_id,
           previous_run_id, actor, reason, occurred_at, evidence_reference)
        VALUES
          (@event_id, 'PROMOTE_AUTOMATED', @release_id, @run_id,
           (SELECT ANY_VALUE(previous_release_id) FROM `{resources.current_release}`
            WHERE singleton = TRUE),
           (SELECT ANY_VALUE(previous_run_id) FROM `{resources.current_release}`
            WHERE singleton = TRUE),
           'github-actions-protected', 'approved Stage 04 shadow promotion',
           CURRENT_TIMESTAMP(), @decision_reference)
        """,
        _config(
            *common,
            bigquery.ScalarQueryParameter("event_id", "STRING", event_id),
            bigquery.ScalarQueryParameter(
                "decision_reference", "STRING", decision_reference
            ),
        ),
    )
    published = _rows(
        client,
        f"""
        SELECT COUNT(*) AS row_count, COUNT(DISTINCT indicator_id) AS indicator_count,
               COUNTIF(release_id != @release_id OR run_id != @run_id) AS wrong_identity,
               COUNTIF(source_hash != @source_hash) AS source_hash_mismatches
        FROM `{resources.published_view}`
        """,
        _config(
            *common,
            bigquery.ScalarQueryParameter(
                "source_hash", "STRING", decision.source_hash.upper()
            ),
        ),
    )[0]
    if (
        int(published["row_count"]) != 3014
        or int(published["indicator_count"]) != 516
        or int(published["wrong_identity"]) != 0
        or int(published["source_hash_mismatches"]) != 0
    ):
        raise ValueError("Published view parity failed after promotion")

    return PromotionEvidence(
        status="BIGQUERY_PROMOTED_PENDING_RUNTIME_VERIFICATION",
        release_id=release_id,
        run_id=run_id,
        row_count=3014,
        indicator_count=516,
        validation_gate_count=5,
        source_hash_match=True,
        fail_closed_view_applied=True,
        pointer_updated=True,
        published_view_updated=True,
        event_recorded=True,
        maximum_bytes_billed=BIGQUERY_MAXIMUM_BYTES_BILLED,
    )
