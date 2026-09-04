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
    assert all(row["synthetic"] == "true" for row in rows)


def test_demo_file_contains_no_sensitive_columns():
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        columns = set(csv.DictReader(handle).fieldnames or ())
    assert SENSITIVE_COLUMNS.isdisjoint(columns)
