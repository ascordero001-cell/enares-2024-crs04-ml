from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from enares.stage04.shadow_pipeline import (
    PipelineInputContract,
    prepare_authorized_aggregate,
)

ROOT = Path(__file__).resolve().parents[1]
AGGREGATE = ROOT / "app/data/v0_authorized_full_indicator_estimates.csv"
MANIFEST = ROOT / "app/data/v0_authorized_full_indicator_estimates.manifest.json"
REGISTRY = ROOT / "docs/stage04/v0_drive_hash_manifest.md"
WORKFLOW = ROOT / ".github/workflows/stage04-shadow-prepare.yml"
DECISION_COMMIT = "b9f79290d71c85b15fa92be17d090f6fa0ac990c"


def _contract() -> PipelineInputContract:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return PipelineInputContract(
        release_id="enares2024-crs04-v0-shadow-001",
        run_id="pr-b-full-v0-authorized-20260916",
        aggregate_sha256=manifest["sha256"],
        manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        parent_sha256=manifest["parent_sha256"],
        expected_row_count=3014,
        expected_indicator_count=516,
        decision_reference=(
            "https://github.com/ascordero001-cell/enares-2024-crs04-ml/"
            "issues/43#issuecomment-5738454716"
        ),
        decision_commit=DECISION_COMMIT,
    )


def test_preparation_verifies_all_rows_and_emits_only_safe_evidence() -> None:
    evidence = prepare_authorized_aggregate(
        _contract(),
        aggregate_path=AGGREGATE,
        manifest_path=MANIFEST,
        approval_registry_path=REGISTRY,
    )
    assert evidence.status == "PASS_PREPARED_NO_CLOUD_MUTATION"
    assert evidence.row_count == 3014
    assert evidence.indicator_count == 516
    assert evidence.module_row_counts == {
        "3.1": 1170,
        "3.2": 389,
        "3.3": 123,
        "3.4": 749,
        "3.5": 457,
        "3.6": 126,
    }
    assert evidence.synthetic_rows == 0
    assert evidence.non_approved_rows == 0
    serialized = evidence.as_json() + evidence.as_markdown()
    assert str(AGGREGATE) not in serialized
    assert "indicator_name" not in serialized


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("release_id", "__UNPROMOTED__"),
        ("run_id", "bad id"),
        ("aggregate_sha256", "not-a-hash"),
        ("decision_commit", "short"),
        ("decision_reference", "free text approval"),
    ],
)
def test_contract_rejects_untraceable_or_reserved_values(field: str, value: str) -> None:
    original = _contract()
    replacements = {
        "release_id": replace(original, release_id=value),
        "run_id": replace(original, run_id=value),
        "aggregate_sha256": replace(original, aggregate_sha256=value),
        "decision_commit": replace(original, decision_commit=value),
        "decision_reference": replace(original, decision_reference=value),
    }
    contract = replacements[field]
    with pytest.raises(ValueError):
        contract.validate()


def test_missing_manual_input_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="manually authorized"):
        prepare_authorized_aggregate(
            _contract(),
            aggregate_path=tmp_path / "missing.csv",
            manifest_path=MANIFEST,
            approval_registry_path=REGISTRY,
        )


def test_changed_aggregate_is_rejected_before_repository_read(tmp_path: Path) -> None:
    changed = tmp_path / AGGREGATE.name
    changed.write_bytes(AGGREGATE.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="Aggregate SHA-256"):
        prepare_authorized_aggregate(
            _contract(),
            aggregate_path=changed,
            manifest_path=MANIFEST,
            approval_registry_path=REGISTRY,
        )


def test_manifest_must_be_bound_to_contract(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["indicator_count"] = 515
    changed_manifest = tmp_path / MANIFEST.name
    changed_manifest.write_text(json.dumps(payload), encoding="utf-8")
    contract = replace(
        _contract(),
        manifest_sha256=hashlib.sha256(changed_manifest.read_bytes()).hexdigest(),
    )
    with pytest.raises(ValueError, match="indicator count"):
        prepare_authorized_aggregate(
            contract,
            aggregate_path=AGGREGATE,
            manifest_path=changed_manifest,
            approval_registry_path=REGISTRY,
        )


def test_workflow_is_manual_fail_closed_and_stops_before_cloud() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in workflow
    assert "pull_request:" not in workflow
    assert "stage04-private-input" in workflow
    assert "stage04-safe-evidence" in workflow
    assert "fetch-depth: 0" in workflow
    assert "git merge-base --is-ancestor" in workflow
    assert "google-github-actions/auth" not in workflow
    assert "gcloud " not in workflow
    assert "bq " not in workflow
    assert "environment:" not in workflow
    assert "no load, query, promotion, IAM, traffic or publication" in workflow
