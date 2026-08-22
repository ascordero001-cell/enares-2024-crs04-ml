"""Generate the complete Stage 03 section 3.2 shadow model and assertions.

The formulas are a direct transcription of the ordered SPSS-authority
implementation in notebook 02. The generator keeps the SQLX reproducible and
exposes a pure contract that unit tests can inspect.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


MODEL_OUTPUT = Path(
    "dataform/definitions/analytical/analytical_crs04_stage32_v0_5.sqlx"
)
QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage32_shadow_quality.sqlx"
)
PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage32_shadow_v0_parity.sqlx"
)

KEY_DESIGN_COLUMNS = [
    "ID",
    "COLEGIAL_ID",
    "FACTOR_ALUMNOS",
    "CCDD",
    "SEXO",
    "AREA",
]


def any_one(names: Iterable[str]) -> str:
    return "(" + " OR ".join(f"`{name}` = 1" for name in names) + ")"


def household_aggressor_expressions(
    stem: str, item_count: int, gateway: str, kind: str
) -> dict[str, str]:
    """Return the eight published aggressor groups for one violence type."""

    groups = {
        1: [1],
        2: [2],
        3: [3],
        4: [4],
        5: [5, 6],
        6: [9, 10],
        7: [18, 19, 20],
        8: [7, 8, 11, 12, 13, 14, 15, 16, 17],
    }
    expressions: dict[str, str] = {}
    for group, codes in groups.items():
        hits = []
        code_list = ",".join(map(str, codes))
        for index in range(1, item_count + 1):
            item = f"{stem}_{index}"
            first_person = f"{stem}A_{index}"
            second_person = f"{stem}E_{index}"
            first_confirm = f"{stem}C_{index}"
            first_detail = f"{stem}D_{index}"
            second_confirm = f"{stem}F_{index}"
            if group <= 4:
                who = (
                    f"({first_person} IN ({code_list}) "
                    f"OR {second_person} IN ({code_list}))"
                )
            elif group == 7:
                who = (
                    f"(({first_person} IN (18,20) "
                    f"AND {first_confirm} = 1 AND {first_detail} = 1) "
                    f"OR {first_person} = 19 "
                    f"OR ({second_person} IN (18,19,20) "
                    f"AND {second_confirm} = 1))"
                )
            else:
                who = (
                    f"(({first_person} IN ({code_list}) "
                    f"AND {first_confirm} = 1 AND {first_detail} = 1) "
                    f"OR ({second_person} IN ({code_list}) "
                    f"AND {second_confirm} = 1))"
                )
            hits.append(f"({item} = 1 AND {gateway} = 1 AND {who})")
        expressions[f"AG_{kind}_H_{group:02d}"] = (
            "CASE WHEN " + " OR ".join(hits) + " THEN 1 ELSE 0 END"
        )
    return expressions


def build_stage32_contract() -> tuple[set[str], list[tuple[str, dict[str, str]]]]:
    """Return raw inputs and the six ordered SPSS 3.2 expression blocks."""

    raw_inputs = {"SEXO", "C3P203", "C3P207", "C3P121"}
    household_forms: dict[str, str] = {}
    for stem, item_count, gateway in [
        ("C3P201", 11, "C3P203"),
        ("C3P205", 7, "C3P207"),
    ]:
        for index in range(1, item_count + 1):
            item = f"{stem}_{index}"
            first_person = f"{stem}A_{index}"
            second_person = f"{stem}E_{index}"
            first_confirm = f"{stem}C_{index}"
            first_detail = f"{stem}D_{index}"
            second_confirm = f"{stem}F_{index}"
            raw_inputs.update(
                {
                    item,
                    first_person,
                    second_person,
                    first_confirm,
                    first_detail,
                    second_confirm,
                }
            )
            valid_aggressor = (
                f"({first_person} IN (1,2,3,4,19) "
                f"OR {second_person} IN (1,2,3,4,19) "
                f"OR ({first_person} IS NOT NULL "
                f"AND {first_person} NOT IN (1,2,3,4,19) "
                f"AND {first_confirm} = 1 AND {first_detail} = 1) "
                f"OR ({second_person} IS NOT NULL "
                f"AND {second_person} NOT IN (1,2,3,4,19) "
                f"AND {second_confirm} = 1))"
            )
            household_forms[f"{stem}_{index}_1"] = (
                f"CASE WHEN SEXO IN (1,2) AND {item} = 1 "
                f"AND {gateway} = 1 AND {valid_aggressor} "
                "THEN 1 ELSE 0 END"
            )

    personal_hit = " OR ".join(
        f"(C3P216A_{index} = 1 AND C3P216A_{index}C = 1)"
        for index in range(1, 7)
    )
    induced_hit = " OR ".join(
        f"(C3P216C_{index} = 1 AND C3P216C_{index}C = 1)"
        for index in range(1, 6)
    )
    for index in range(1, 7):
        raw_inputs.update({f"C3P216A_{index}", f"C3P216A_{index}C"})
    for index in range(1, 6):
        raw_inputs.update({f"C3P216C_{index}", f"C3P216C_{index}C"})

    main_indicators = {
        "VP_HOGAR": (
            "CASE WHEN "
            + any_one(f"C3P201_{index}_1" for index in range(1, 12))
            + " THEN 1 ELSE 0 END"
        ),
        "VF_HOGAR": (
            "CASE WHEN "
            + any_one(f"C3P205_{index}_1" for index in range(1, 8))
            + " THEN 1 ELSE 0 END"
        ),
        "VF_HOGAR_01": "CASE WHEN C3P121 = 1 THEN 1 ELSE 0 END",
        "VF_HOGAR_03": (
            f"CASE WHEN ({personal_hit}) OR ({induced_hit}) "
            "THEN 1 ELSE 0 END"
        ),
    }

    combinations = {
        "VN_HOGAR1": (
            "CASE WHEN VF_HOGAR_01 = 1 OR VF_HOGAR_03 = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "INDICADOR_8_3_6": (
            "CASE WHEN VP_HOGAR = 1 OR VF_HOGAR = 1 "
            "OR VF_HOGAR_01 = 1 OR VF_HOGAR_03 = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "VP_o_VF_HOGAR": (
            "CASE WHEN VP_HOGAR = 1 OR VF_HOGAR = 1 THEN 1 ELSE 0 END"
        ),
        "VP_VF_HOGAR": (
            "CASE WHEN VP_HOGAR = 1 AND VF_HOGAR = 1 THEN 1 ELSE 0 END"
        ),
    }
    published_alias = {"Solap_VP_VF_H__Coexistencia": "VP_VF_HOGAR"}

    icvac = {
        "VP_ICVAC_401_ATERRORIZAR": (
            "CASE WHEN "
            + any_one(["C3P201_6_1", "C3P201_7_1", "C3P201_9_1"])
            + " THEN 1 ELSE 0 END"
        ),
        "VP_ICVAC_402_HOSTIGAR_HUMILLAR": (
            "CASE WHEN "
            + any_one(f"C3P201_{index}_1" for index in range(1, 6))
            + " THEN 1 ELSE 0 END"
        ),
        "VP_ICVAC_203_AISLAMIENTO": (
            "CASE WHEN "
            + any_one(["C3P201_8_1", "C3P201_10_1"])
            + " THEN 1 ELSE 0 END"
        ),
        "VP_ICVAC_409_OTROS": (
            "CASE WHEN C3P201_11_1 = 1 THEN 1 ELSE 0 END"
        ),
        "VF_ICVAC_201_AGRESION_GRAVE": (
            "CASE WHEN "
            + any_one(["C3P205_5_1", "C3P205_6_1"])
            + " THEN 1 ELSE 0 END"
        ),
        "VF_ICVAC_202_AGRESION_LEVE": (
            "CASE WHEN "
            + any_one(f"C3P205_{index}_1" for index in range(1, 5))
            + " THEN 1 ELSE 0 END"
        ),
        "VF_ICVAC_209_OTROS": (
            "CASE WHEN C3P205_7_1 = 1 THEN 1 ELSE 0 END"
        ),
    }

    aggressors = {
        **household_aggressor_expressions("C3P201", 11, "C3P203", "VP"),
        **household_aggressor_expressions("C3P205", 7, "C3P207", "VF"),
    }

    blocks = [
        ("32_hogar_formas", household_forms),
        ("32_hogar_principales", main_indicators),
        ("32_hogar_combinaciones_base", combinations),
        ("32_hogar_aliases_publicados", published_alias),
        ("32_hogar_icvac", icvac),
        ("321_hogar_agresores", aggressors),
    ]
    return raw_inputs, blocks


def output_columns(blocks: list[tuple[str, dict[str, str]]]) -> list[str]:
    return [column for _, expressions in blocks for column in expressions]


def render_model() -> str:
    raw_inputs, blocks = build_stage32_contract()
    raw_only = sorted(set(raw_inputs) - set(KEY_DESIGN_COLUMNS))
    base_columns = KEY_DESIGN_COLUMNS + raw_only
    base_select = ",\n".join(f"    `{column}`" for column in base_columns)

    ctes = [
        "base AS (\n"
        "  SELECT\n"
        f"{base_select}\n"
        '  FROM ${ref("cleaned_crs04_merged_adolescents_v0_5")}\n'
        ")"
    ]
    previous = "base"
    for index, (block_name, expressions) in enumerate(blocks, start=1):
        cte_name = f"block_{index:02d}_{block_name}"
        derived = ",\n".join(
            f"    {expression} AS `{column}`"
            for column, expression in expressions.items()
        )
        ctes.append(
            f"{cte_name} AS (\n"
            "  SELECT\n"
            "    *,\n"
            f"{derived}\n"
            f"  FROM {previous}\n"
            ")"
        )
        previous = cte_name

    final_columns = KEY_DESIGN_COLUMNS + output_columns(blocks)
    final_select = ",\n".join(f"  `{column}`" for column in final_columns)
    return f'''config {{
  type: "table",
  schema: dataform.projectConfig.vars.analyticalDataset,
  name: "analytical_crs04_stage32_v0_5",
  description: "Stage 03 section 3.2 SPSS-authority shadow model.",
  tags: ["stage03", "analytical", "stage32", "shadow"]
}}

WITH
{",\n\n".join(ctes)}

SELECT
{final_select}
FROM {previous}
'''


def render_quality_assertion() -> str:
    _, blocks = build_stage32_contract()
    binary_condition = "\n    OR ".join(
        f"`{column}` NOT IN (0, 1) OR `{column}` IS NULL"
        for column in output_columns(blocks)
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage32", "quality"]
}}

WITH
candidate AS (
  SELECT *
  FROM ${{ref("analytical_crs04_stage32_v0_5")}}
),

duplicate_keys AS (
  SELECT ID, COLEGIAL_ID
  FROM candidate
  GROUP BY ID, COLEGIAL_ID
  HAVING COUNT(*) > 1
),

checks AS (
  SELECT "row_count" AS check_name, ABS(COUNT(*) - 18807) AS violation_count
  FROM candidate
  HAVING COUNT(*) != 18807

  UNION ALL

  SELECT "null_keys", COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL)
  FROM candidate
  HAVING COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL) > 0

  UNION ALL

  SELECT "duplicate_key_groups", COUNT(*)
  FROM duplicate_keys
  HAVING COUNT(*) > 0

  UNION ALL

  SELECT "survey_design_fields", COUNTIF(
    FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0
    OR CCDD IS NULL OR SEXO IS NULL OR AREA IS NULL
  )
  FROM candidate
  HAVING COUNTIF(
    FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0
    OR CCDD IS NULL OR SEXO IS NULL OR AREA IS NULL
  ) > 0

  UNION ALL

  SELECT "binary_outputs", COUNTIF(
    {binary_condition}
  )
  FROM candidate
  HAVING COUNTIF(
    {binary_condition}
  ) > 0
)

SELECT *
FROM checks
'''


def render_parity_assertion() -> str:
    _, blocks = build_stage32_contract()
    columns = output_columns(blocks)
    reference_select = ",\n".join(f"    `{column}`" for column in columns)
    candidate_select = ",\n".join(f"    `{column}`" for column in columns)
    comparisons = "\n  OR ".join(
        f"candidate.`{column}` IS DISTINCT FROM reference.`{column}`"
        for column in columns
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage32", "parity"]
}}

WITH
reference AS (
  SELECT
    CAST(ID AS INT64) AS ID,
    CAST(COLEGIAL_ID AS INT64) AS COLEGIAL_ID,
{reference_select}
  FROM ${{ref("analytical_crs04_adolescents")}}
),

candidate AS (
  SELECT
    ID,
    COLEGIAL_ID,
{candidate_select}
  FROM ${{ref("analytical_crs04_stage32_v0_5")}}
)

SELECT
  COALESCE(candidate.ID, reference.ID) AS ID,
  COALESCE(candidate.COLEGIAL_ID, reference.COLEGIAL_ID) AS COLEGIAL_ID
FROM candidate
FULL OUTER JOIN reference
  USING (ID, COLEGIAL_ID)
WHERE
  candidate.ID IS NULL
  OR reference.ID IS NULL
  OR {comparisons}
'''


def main() -> None:
    _, blocks = build_stage32_contract()
    outputs = [
        (MODEL_OUTPUT, render_model()),
        (QUALITY_OUTPUT, render_quality_assertion()),
        (PARITY_OUTPUT, render_parity_assertion()),
    ]
    for path, content in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8", newline="\n")
        print(f"Generated: {path}")
    print(f"Blocks generated: {len(blocks)}")
    print(f"Derived columns generated: {len(output_columns(blocks))}")


if __name__ == "__main__":
    main()
