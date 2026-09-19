from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from enares.stage04.cloud_promotion import (
    PromotionResources,
    load_promotion_decision,
    promote_reconciled_release,
)

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "stage04-shadow-promote.yml"


def _decision(path: Path, **overrides: Any) -> Path:
    payload = {
        "schema_version": "stage04-promotion-decision-v1",
        "action": "APPROVE_AUTHENTICATED_SHADOW_PROMOTION",
        "status": "APPROVED",
        "reviewer": "ritaricaldi-cpu",
        "scope": "CONTROLLED_SHADOW",
        "release_id": "enares2024-crs04-v0-shadow-001",
        "run_id": "pr-b-full-v0-authorized-20260916",
        "source_hash": "A" * 64,
        "reconciliation_run_url": (
            "https://github.com/ascordero001-cell/enares-2024-crs04-ml/"
            "actions/runs/35421445001"
        ),
        "allow_public_access": False,
        "allow_cutover": False,
    }
    payload.update(overrides)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _load(path: Path):
    return load_promotion_decision(
        path,
        release_id="enares2024-crs04-v0-shadow-001",
        run_id="pr-b-full-v0-authorized-20260916",
        source_hash="A" * 64,
        reconciliation_run_url=(
            "https://github.com/ascordero001-cell/enares-2024-crs04-ml/"
            "actions/runs/35421445001"
        ),
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("status", "PENDING"),
        ("reviewer", "ana"),
        ("allow_public_access", True),
        ("allow_cutover", True),
        ("run_id", "different-run"),
    ],
)
def test_promotion_decision_fails_closed(field: str, value: Any, tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not match"):
        _load(_decision(tmp_path / "decision.json", **{field: value}))


class _Job:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    def result(self) -> list[dict[str, Any]]:
        return self.rows


class _Client:
    def __init__(self) -> None:
        self.queries: list[tuple[str, Any]] = []
        self.hash_results: list[list[str]] = [["hash-a"] * 3014, ["hash-a"] * 3014]

    def query(self, query: str, *, job_config: Any) -> _Job:
        self.queries.append((query, job_config))
        if "source_hash_mismatches" in query and "published" not in query:
            return _Job(
                [
                    {
                        "row_count": 3014,
                        "indicator_count": 516,
                        "source_hash_mismatches": 0,
                        "invalid_rows": 0,
                    }
                ]
            )
        if "approved_count" in query:
            return _Job([{"approved_count": 1}])
        if "validation_name, validation_status" in query:
            return _Job(
                [
                    {"validation_name": name, "validation_status": "PASS"}
                    for name in (
                        "technical",
                        "v0_parity",
                        "privacy",
                        "release_consistency",
                        "query_cost_cap",
                    )
                ]
            )
        if "wrong_identity" in query:
            return _Job(
                [
                    {
                        "row_count": 3014,
                        "indicator_count": 516,
                        "wrong_identity": 0,
                        "source_hash_mismatches": 0,
                    }
                ]
            )
        if "AS row_hashes" in query:
            return _Job([{"row_hashes": self.hash_results.pop(0)}])
        return _Job([])


def test_promotion_is_fail_closed_and_uses_one_guardrail(tmp_path: Path) -> None:
    decision = _load(_decision(tmp_path / "decision.json"))
    client = _Client()
    project = "enares-2024-crs04"
    evidence = promote_reconciled_release(
        client=client,
        decision=decision,
        resources=PromotionResources(
            outputs_table=f"{project}.shadow_outputs.indicator_estimates",
            release_registry=f"{project}.shadow_ops.release_registry",
            validation_results=f"{project}.shadow_ops.validation_results",
            current_release=f"{project}.shadow_ops.current_release",
            promotion_events=f"{project}.shadow_ops.promotion_events",
            published_view=f"{project}.shadow_published.v_dashboard_current",
        ),
        decision_reference="https://github.com/example/decision",
    )

    assert evidence.status == "BIGQUERY_PROMOTED_PENDING_RUNTIME_VERIFICATION"
    assert evidence.row_hash_parity is True
    queries = [query for query, _ in client.queries]
    fail_closed = next(i for i, query in enumerate(queries) if "WHERE FALSE" in query)
    pointer = next(i for i, query in enumerate(queries) if "DELETE FROM" in query)
    promoted = next(
        i
        for i, query in enumerate(queries)
        if "CREATE OR REPLACE VIEW" in query and "WHERE FALSE" not in query
    )
    assert fail_closed < pointer < promoted
    assert "BEGIN TRANSACTION" in queries[pointer]
    assert "IS DISTINCT FROM @release_id" in queries[pointer]
    assert "previous_release_id" in next(
        query for query in queries if "PROMOTE_AUTOMATED" in query
    )
    assert all(config.maximum_bytes_billed == 10_485_760 for _, config in client.queries)
    assert all(config.use_query_cache is False for _, config in client.queries)


def test_promotion_fails_closed_when_exact_projection_parity_differs(
    tmp_path: Path,
) -> None:
    decision = _load(_decision(tmp_path / "decision.json"))
    client = _Client()
    client.hash_results = [["expected"] * 3014, ["actual"] * 3014]
    project = "enares-2024-crs04"

    with pytest.raises(ValueError, match="row-hash parity"):
        promote_reconciled_release(
            client=client,
            decision=decision,
            resources=PromotionResources(
                outputs_table=f"{project}.shadow_outputs.indicator_estimates",
                release_registry=f"{project}.shadow_ops.release_registry",
                validation_results=f"{project}.shadow_ops.validation_results",
                current_release=f"{project}.shadow_ops.current_release",
                promotion_events=f"{project}.shadow_ops.promotion_events",
                published_view=f"{project}.shadow_published.v_dashboard_current",
            ),
            decision_reference="https://github.com/example/decision",
        )

    fail_closed_queries = [
        query for query, _ in client.queries if "WHERE FALSE" in query
    ]
    assert len(fail_closed_queries) == 2


def test_promotion_workflow_preserves_human_gate_and_private_runtime() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "if: github.ref == 'refs/heads/main'" in workflow
    assert "name: stage04-shadow-mutation" in workflow
    assert "decision_commit" in workflow
    assert "docs/stage04/decisions/" in workflow
    assert "APPROVE_AUTHENTICATED_SHADOW_PROMOTION" not in workflow
    assert "--no-traffic" in workflow
    assert "Candidate minimum scale is not zero" in workflow
    assert "Candidate maximum scale is not one" in workflow
    assert "Candidate concurrency is not six" in workflow
    assert 'anonymousStatus.Trim() -ne "403"' in workflow
    assert 'authenticatedStatus.Trim() -ne "200"' in workflow
    assert '--max 1' in workflow
    assert "exactly 100 percent traffic" in workflow
    assert "Cloud Run minimum scale is not zero" in workflow
    assert '"allUsers"' in workflow
    assert '"allAuthenticatedUsers"' in workflow
    assert "--allow-unauthenticated" not in workflow
    assert "--no-allow-unauthenticated" not in workflow


def test_failure_evidence_uses_runner_native_shell() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    outcome_step = workflow.split("- name: Record redacted workflow outcome", 1)[1]
    outcome_step = outcome_step.split("- name: Upload redacted promotion evidence", 1)[0]

    assert "if: always()" in outcome_step
    assert "shell: powershell" in outcome_step
    assert "shell: pwsh" not in outcome_step


def test_promotion_workflow_uses_only_runner_native_powershell() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "shell: pwsh" not in workflow
    assert workflow.count("shell: powershell") == 6
    assert "SkipHttpErrorCheck" not in workflow
    assert "curl.exe --silent --show-error" in workflow
    assert "[IO.File]::WriteAllText" in workflow
