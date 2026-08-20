import csv
import hashlib
from pathlib import Path

import yaml


SOURCE_DIR = Path("docs/stage03/contracts/v0")
CONFIG_DIR = Path("configs")

SOURCE_HASHES = {
    "diccionario_indicadores.csv":
        "f5fd6979a19ebc9f510c307705b1e7de12556a8f5a81ddbc566e97347337bd2c",
    "stage3_r_tabulation_specs.csv":
        "af312a53f19718b00e3307e02fc6c91b8720b7eeac4139493529aaf81f368082",
    "stage3_skip_map.csv":
        "bc63719e9de021ff13af5098ecc39f337eaab1e20f05a5ffa931311c74199792",
    "stage3_spss_block_lineage.csv":
        "2b698ab611a6e0d2abc17303a940530b07f4dab32f1e0d7ef58fc56bc7f47f84",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(name: str):
    path = SOURCE_DIR / name

    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def clean(value):
    if value is None:
        return None

    value = value.strip()
    return value if value else None


for filename, expected_hash in SOURCE_HASHES.items():
    actual_hash = sha256(SOURCE_DIR / filename)

    if actual_hash != expected_hash:
        raise RuntimeError(
            f"{filename}: SHA-256 changed: {actual_hash}"
        )

specifications = read_csv("stage3_r_tabulation_specs.csv")
dictionary = read_csv("diccionario_indicadores.csv")
skip_rules = read_csv("stage3_skip_map.csv")

spec_names = [row["indicator_name"].strip() for row in specifications]
dictionary_names = [
    row["indicator_name"].strip()
    for row in dictionary
]

if len(specifications) != 516:
    raise RuntimeError(
        f"Expected 516 specifications, found {len(specifications)}"
    )

if len(set(spec_names)) != 516:
    raise RuntimeError("Specification indicator names are not unique")

if set(spec_names) != set(dictionary_names):
    raise RuntimeError(
        "Specification and dictionary indicator sets differ"
    )

indicator_fields = [
    "indicator_name",
    "label",
    "module",
    "data_variable",
    "variable_type",
    "statistic_type",
    "target_category",
    "status",
    "domain_variable",
    "domain_value",
    "dimensions",
    "ci_method",
    "ci_methods_by_dimension",
    "count_method",
    "count_methods_by_dimension",
    "domain_mode",
    "domain_modes_by_dimension",
    "critical_mode",
    "critical_modes_by_dimension",
    "department_categories",
]

indicators_contract = {
    "schema_version": 1,
    "contract_version": "v0.5-shadow",
    "authority": "SPSS syntax and validated V0 specification",
    "source": "docs/stage03/contracts/v0/stage3_r_tabulation_specs.csv",
    "indicator_count": len(specifications),
    "indicators": [
        {
            field: clean(row.get(field))
            for field in indicator_fields
        }
        for row in specifications
    ],
}

skip_fields = [
    "block",
    "gateway_var",
    "open_value",
    "dependent_vars",
    "recode",
    "keep_null_when",
    "source_module",
]

skip_contract = {
    "schema_version": 1,
    "contract_version": "v0.5-shadow",
    "authority": "SPSS syntax and validated V0 skip map",
    "source": "docs/stage03/contracts/v0/stage3_skip_map.csv",
    "rule_count": len(skip_rules),
    "rules": [
        {
            field: clean(row.get(field))
            for field in skip_fields
        }
        for row in skip_rules
    ],
}

CONFIG_DIR.mkdir(exist_ok=True)

(CONFIG_DIR / "indicators_crs04.yaml").write_text(
    yaml.safe_dump(
        indicators_contract,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    ),
    encoding="utf-8",
    newline="\n",
)

(CONFIG_DIR / "skip_logic_crs04.yaml").write_text(
    yaml.safe_dump(
        skip_contract,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    ),
    encoding="utf-8",
    newline="\n",
)

print(f"Indicators generated: {len(specifications)}")
print(f"Skip rules generated: {len(skip_rules)}")