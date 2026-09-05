import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "app" / "data"
CSV_PATH = DATA_DIR / "demo_indicator_estimates.csv"
MANIFEST_PATH = DATA_DIR / "demo_indicator_estimates.manifest.json"
V0_CSV_PATH = DATA_DIR / "v0_authorized_indicator_estimates.csv"
V0_MANIFEST_PATH = DATA_DIR / "v0_authorized_indicator_estimates.manifest.json"
SENSITIVE_COLUMNS = {
    "respondent_id",
    "person_id",
    "child_id",
    "nna_id",
    "name",
    "birth_date",
    "address",
    "phone",
    "email",
    "latitude",
    "longitude",
    "raw_record",
}
AUTHORIZED_HASH = "15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4"


def test_demo_manifest_matches_file_and_is_explicitly_synthetic():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    digest = hashlib.sha256(CSV_PATH.read_bytes()).hexdigest()
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert manifest["synthetic"] is True
    assert manifest["schema_version"]
    assert manifest["file_name"] == CSV_PATH.name
    assert manifest["sha256"] == digest
    assert manifest["row_count"] == len(rows)
    assert manifest["composition"] == {"synthetic_rows": 3}
    assert all(row["synthetic"] == "true" for row in rows)


def test_v0_authorized_manifest_matches_single_aggregate_file():
    manifest = json.loads(V0_MANIFEST_PATH.read_text(encoding="utf-8"))
    digest = hashlib.sha256(V0_CSV_PATH.read_bytes()).hexdigest()
    with V0_CSV_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert manifest["file_name"] == V0_CSV_PATH.name
    assert manifest["sha256"] == digest
    assert manifest["row_count"] == len(rows) == 1
    assert manifest["synthetic"] is False
    assert manifest["data_classification"] == "AUTHORIZED_AGGREGATE_ONLY"
    assert manifest["source_hash"] == AUTHORIZED_HASH
    assert all(row["synthetic"] == "false" for row in rows)
    assert all(row["source_hash"] == AUTHORIZED_HASH for row in rows)


def test_demo_file_contains_no_sensitive_columns():
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        columns = set(csv.DictReader(handle).fieldnames or ())
    assert SENSITIVE_COLUMNS.isdisjoint(columns)


def test_v0_authorized_file_contains_no_sensitive_columns():
    with V0_CSV_PATH.open(encoding="utf-8", newline="") as handle:
        columns = set(csv.DictReader(handle).fieldnames or ())
    assert SENSITIVE_COLUMNS.isdisjoint(columns)
