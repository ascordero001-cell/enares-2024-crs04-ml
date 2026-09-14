import csv
import hashlib
import json
import os
from pathlib import Path

import pytest

from enares.stage04.authorized_extract import rederive_authorized_extract
from enares.stage04.authorized_scopes import D09_PAIRS
from enares.stage04.repository import AuthorizedAggregateRepository

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "app" / "data" / "v0_authorized_etapa1_indicator_estimates.csv"
MANIFEST = (
    ROOT / "app" / "data" / "v0_authorized_etapa1_indicator_estimates.manifest.json"
)
REGISTRY = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"
PARENT_SHA256 = "15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4"


def _rows():
    with EXTRACT.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_etapa1_extract_manifest_binds_exact_file_and_parent():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["row_count"] == 35
    assert manifest["synthetic"] is False
    assert manifest["source_kind"] == "AUTHORIZED_V0_EXTRACT"
    assert manifest["source_hash"] == PARENT_SHA256
    assert manifest["parent_sha256"] == PARENT_SHA256
    assert manifest["sha256"] == hashlib.sha256(EXTRACT.read_bytes()).hexdigest()
    assert manifest["sha256"].upper() != PARENT_SHA256


def test_etapa1_extract_contains_only_closed_d01_d09_d11_scope():
    rows = _rows()
    by_indicator = {}
    for row in rows:
        by_indicator.setdefault(row["indicator_id"], []).append(row)

    assert len(by_indicator["Componentes"]) == 10
    assert len(by_indicator["CONS_ATENCION_SALUD"]) == 22
    assert {key: len(by_indicator[key]) for key in (
        "C3P223_10_1",
        "Agresor_VS_12M__AG_01",
        "C3P213",
    )} == {
        "C3P223_10_1": 1,
        "Agresor_VS_12M__AG_01": 1,
        "C3P213": 1,
    }
    assert set(by_indicator) == {
        "Componentes",
        "CONS_ATENCION_SALUD",
        "C3P223_10_1",
        "Agresor_VS_12M__AG_01",
        "C3P213",
    }
    assert all(row["synthetic"] == "false" for row in rows)


def test_d09_extract_has_exact_pairs_aliases_and_thirteen_reference_cells():
    rows = [row for row in _rows() if row["indicator_id"] == "CONS_ATENCION_SALUD"]
    assert {(row["disaggregation"], row["category"]) for row in rows} == D09_PAIRS
    assert sum(row["cv_flag"] == "true" for row in rows) == 13
    assert all(row["suppress_flag"] == "false" for row in rows)
    assert "Área y sexo" not in {row["disaggregation"] for row in rows}
    assert "Lengua materna" not in {row["disaggregation"] for row in rows}


def test_authorized_repository_accepts_all_etapa1_modules():
    repository = AuthorizedAggregateRepository(EXTRACT, MANIFEST, REGISTRY)
    counts = {
        module: len(repository.list_estimates(module))
        for module in ("3.1", "3.3", "3.4", "3.5", "3.6")
    }
    assert counts == {"3.1": 10, "3.3": 1, "3.4": 1, "3.5": 22, "3.6": 1}


def test_etapa1_extract_rederives_byte_for_byte_from_private_parent(tmp_path):
    parent_value = os.environ.get("ENARES_V0_PARENT_AGGREGATE")
    if not parent_value:
        pytest.skip("Private V0 parent path is not available in CI")
    parent = Path(parent_value)
    output = tmp_path / "rederived.csv"
    rederive_authorized_extract(
        parent,
        EXTRACT,
        output,
        expected_parent_file_sha256=PARENT_SHA256,
        approved_parent_sha256=PARENT_SHA256,
    )
    assert output.read_bytes() == EXTRACT.read_bytes()
