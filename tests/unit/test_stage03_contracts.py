import csv
import hashlib
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/stage03/contracts/v0"
CONFIGS = ROOT / "configs"

EXPECTED_HASHES = {
    "diccionario_indicadores.csv":
        "f5fd6979a19ebc9f510c307705b1e7de12556a8f5a81ddbc566e97347337bd2c",
    "stage3_r_tabulation_specs.csv":
        "af312a53f19718b00e3307e02fc6c91b8720b7eeac4139493529aaf81f368082",
    "stage3_skip_map.csv":
        "bc63719e9de021ff13af5098ecc39f337eaab1e20f05a5ffa931311c74199792",
    "stage3_spss_block_lineage.csv":
        "2b698ab611a6e0d2abc17303a940530b07f4dab32f1e0d7ef58fc56bc7f47f84",
}


def load_csv(name):
    with (SOURCE / name).open(
        encoding="utf-8-sig",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def load_yaml(name):
    return yaml.safe_load(
        (CONFIGS / name).read_text(encoding="utf-8")
    )


def test_frozen_source_hashes():
    for name, expected in EXPECTED_HASHES.items():
        actual = hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
        assert actual == expected


def test_indicator_contract():
    contract = load_yaml("indicators_crs04.yaml")
    indicators = contract["indicators"]
    names = [row["indicator_name"] for row in indicators]

    assert contract["indicator_count"] == 516
    assert len(indicators) == 516
    assert len(set(names)) == 516
    assert all(row["indicator_name"] for row in indicators)
    assert all(row["data_variable"] for row in indicators)


def test_indicator_contract_matches_v0_sources():
    contract = load_yaml("indicators_crs04.yaml")
    yaml_names = {
        row["indicator_name"]
        for row in contract["indicators"]
    }

    specification_names = {
        row["indicator_name"]
        for row in load_csv("stage3_r_tabulation_specs.csv")
    }

    dictionary_names = {
        row["indicator_name"]
        for row in load_csv("diccionario_indicadores.csv")
    }

    assert yaml_names == specification_names
    assert yaml_names == dictionary_names


def test_skip_logic_contract():
    contract = load_yaml("skip_logic_crs04.yaml")
    rules = contract["rules"]

    assert contract["rule_count"] == 13
    assert len(rules) == 13
    assert all(rule["block"] for rule in rules)
    assert all(rule["gateway_var"] for rule in rules)
    assert all(rule["dependent_vars"] for rule in rules)