from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from app.streamlit_app import local_repositories
from enares.stage04.repository import is_verified_authorized_estimate
from enares.stage04.v0_catalog_registry import (
    DICTIONARY_SHA256,
    V0_MODULE_BY_INDICATOR,
)
from enares.stage04.validation import validate_estimates

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "app" / "data"
EXTRACT = DATA / "v0_authorized_full_indicator_estimates.csv"
MANIFEST = DATA / "v0_authorized_full_indicator_estimates.manifest.json"
LEDGER = DATA / "v0_authorized_full_reconciliation_sha256.csv"
PARENT_SHA256 = "15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4"
EXPECTED_MODULE_COUNTS = {
    "3.1": 1170,
    "3.2": 389,
    "3.3": 123,
    "3.4": 749,
    "3.5": 457,
    "3.6": 126,
}


def test_full_v0_manifest_binds_extract_dictionary_and_reconciliation_ledger() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["row_count"] == 3014
    assert manifest["indicator_count"] == 516
    assert manifest["source_hash"] == PARENT_SHA256
    assert manifest["parent_sha256"] == PARENT_SHA256
    assert manifest["dictionary_sha256"] == DICTIONARY_SHA256
    assert manifest["module_row_counts"] == EXPECTED_MODULE_COUNTS
    assert manifest["scope"] == {"A": 2995, "C": 4, "D": 7, "E": 8}
    assert manifest["sha256"] == hashlib.sha256(EXTRACT.read_bytes()).hexdigest()
    assert manifest["reconciliation_sha256"] == hashlib.sha256(
        LEDGER.read_bytes()
    ).hexdigest()


def test_all_3014_rows_reconcile_and_pass_the_runtime_contract() -> None:
    with EXTRACT.open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        ledger_rows = list(csv.DictReader(handle))
    ledger = {
        (row["indicator_id"], row["dimension"], row["category"]): row[
            "parent_row_sha256"
        ]
        for row in ledger_rows
    }
    assert len(source_rows) == len(ledger) == 3014
    assert len({row["indicator_id"] for row in source_rows}) == 516
    assert not any("UNRESOLVED" in value for row in source_rows for value in row.values())

    authorized, _ = local_repositories()
    repository_rows = []
    for module_id, expected_count in EXPECTED_MODULE_COUNTS.items():
        rows = authorized.list_estimates(module_id)
        assert len(rows) == expected_count
        repository_rows.extend(rows)
    by_key = {
        (row.indicator_id, row.disaggregation, row.category): row
        for row in repository_rows
    }
    assert len(by_key) == 3014

    for source in source_rows:
        key = (source["indicator_id"], source["disaggregation"], source["category"])
        assert V0_MODULE_BY_INDICATOR[source["indicator_id"]] == source["module_id"]
        canonical = {
            "indicator_id": source["indicator_id"],
            "dimension": source["disaggregation"],
            "category": source["category"],
            "estimate": source["estimate"],
            "standard_error": source["standard_error"],
            "ci95_lower": source["ci95_lower"],
            "ci95_upper": source["ci95_upper"],
            "cv": source["cv"],
            "n_unweighted": source["n_unweighted"],
        }
        digest = hashlib.sha256(
            json.dumps(
                canonical,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        assert ledger[key] == digest
        row = by_key[key]
        assert is_verified_authorized_estimate(row)
        assert row.synthetic is False
        validate_estimates([row])


def test_authorized_exception_treatments_are_complete() -> None:
    authorized, _ = local_repositories()
    rows = authorized.list_estimates("3.5")
    assert sum(row.quality_status == "CONTEXT_ONLY" for row in rows) == 4
    assert sum(row.indicator_id == "num_consecuencias_fisicas" for row in rows) == 7
    assert not any("[referencial]" in row.category for row in rows)
    assert sum(
        row.indicator_id in {"Solap_VS_12M", "Solap_VS_VIDA"}
        and row.disaggregation in {"2×2", "3×3"}
        for row in rows
    ) == 16
