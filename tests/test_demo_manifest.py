import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "app" / "data"
CSV_PATH = DATA_DIR / "demo_indicator_estimates.csv"
MANIFEST_PATH = DATA_DIR / "demo_indicator_estimates.manifest.json"
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
    assert manifest["composition"]["synthetic_rows"] == 2
    assert manifest["composition"]["authorized_aggregate_rows"] == 1
    assert sum(row["synthetic"] == "true" for row in rows) == 2
    authorized = [row for row in rows if row["synthetic"] == "false"]
    assert len(authorized) == 1
    assert authorized[0]["source_hash"] == AUTHORIZED_HASH


def test_demo_file_contains_no_sensitive_columns():
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        columns = set(csv.DictReader(handle).fieldnames or ())
    assert SENSITIVE_COLUMNS.isdisjoint(columns)
