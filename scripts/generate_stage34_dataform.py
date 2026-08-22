"""Generate the complete Stage 03 section 3.4 shadow model and assertions.

The formulas directly transcribe the ordered SPSS-authority implementation in
notebook 02. Published aliases that depend on household or school aggressor
groups consume the already validated section 3.2 and 3.3 shadow tables.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


MODEL_OUTPUT = Path(
    "dataform/definitions/analytical/analytical_crs04_stage34_v0_5.sqlx"
)
QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage34_shadow_quality.sqlx"
)
PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage34_shadow_v0_parity.sqlx"
)

KEY_DESIGN_COLUMNS = [
    "ID",
    "COLEGIAL_ID",
    "FACTOR_ALUMNOS",
    "CCDD",
    "SEXO",
    "AREA",
]
HOUSEHOLD_DEPENDENCIES = [
    *(f"AG_VP_H_{index:02d}" for index in range(1, 9)),
    *(f"AG_VF_H_{index:02d}" for index in range(1, 9)),
]
SCHOOL_DEPENDENCIES = [
    *(f"AG_VP_E_{index:02d}" for index in range(1, 10)),
    *(f"AG_VF_E_{index:02d}" for index in range(1, 10)),
]


def any_one(names: Iterable[str]) -> str:
    return "(" + " OR ".join(f"`{name}` = 1" for name in names) + ")"


def binary_aggregate(names: Iterable[str]) -> str:
    return "CASE WHEN " + any_one(names) + " THEN 1 ELSE 0 END"


def build_stage34_contract() -> tuple[set[str], list[tuple[str, dict[str, str]]]]:
    """Return raw inputs and the seven ordered SPSS 3.4 expression blocks."""

    raw_inputs = {"SEXO"}
    forms: dict[str, str] = {}
    for index in range(1, 17):
        item = f"C4P248_{index}"
        recent = f"C4P248C_{index}"
        raw_inputs.update({item, recent})
        for aggressor in range(1, 29):
            raw_inputs.add(f"C4P248A_{aggressor}_{index}")
        school_context = (
            f"C4P248A_27_{index} = 1 OR C4P248A_28_{index} = 1"
        )
        household_context = " OR ".join(
            f"C4P248A_{aggressor}_{index} = 1"
            for aggressor in range(1, 18)
        )
        forms[f"P248_{index:02d}_12M"] = (
            f"CASE WHEN {item} = 1 AND {recent} = 1 THEN 1 ELSE 0 END"
        )
        forms[f"C4P248_{index}_1"] = (
            f"CASE WHEN {item} = 1 AND {recent} = 1 "
            f"AND ({school_context}) THEN 1 ELSE 0 END"
        )
        forms[f"C4P248_{index}_1_1"] = (
            f"CASE WHEN {item} = 1 AND ({school_context}) THEN 1 ELSE 0 END"
        )
        forms[f"C4P248_{index}_3"] = (
            f"CASE WHEN {item} = 1 AND {recent} = 1 "
            f"AND ({household_context}) THEN 1 ELSE 0 END"
        )
        forms[f"C4P248_{index}_3_1"] = (
            f"CASE WHEN {item} = 1 AND ({household_context}) "
            "THEN 1 ELSE 0 END"
        )

    main_indicators = {
        "VS_12M": binary_aggregate(
            f"P248_{index:02d}_12M" for index in range(1, 17)
        ),
        "VS_VIDA": binary_aggregate(
            f"C4P248_{index}" for index in range(1, 17)
        ),
        "VS_E": binary_aggregate(
            f"C4P248_{index}_1" for index in range(1, 17)
        ),
        "VS_E_1": binary_aggregate(
            f"C4P248_{index}_1_1" for index in range(1, 17)
        ),
        "VS_H": binary_aggregate(
            f"C4P248_{index}_3" for index in range(1, 17)
        ),
        "VS_H_1": binary_aggregate(
            f"C4P248_{index}_3_1" for index in range(1, 17)
        ),
    }

    icvac_groups = {
        "301": [11],
        "302": [4, 5, 6],
        "303": [1, 2, 3, 7, 8, 9, 10, 13, 14, 15, 16],
        "309": [12],
    }
    cp_groups = {
        "CP01": [1, 2],
        "CP02": [3, 7, 9],
        "CP03": [4, 5, 6, 8],
        "CP04": [10],
        "CP05": [11],
        "CP06": [13],
        "CP07": [14],
        "CP08": [15, 16],
        "CP09": [12],
    }
    grouped_indicators: dict[str, str] = {}
    for code, indices in icvac_groups.items():
        grouped_indicators[f"VS_ICVAC_{code}"] = binary_aggregate(
            f"P248_{index:02d}_12M" for index in indices
        )
        grouped_indicators[f"VS_ICVAC_{code}_VIDA"] = binary_aggregate(
            f"C4P248_{index}" for index in indices
        )
        grouped_indicators[f"VSE_{code}"] = binary_aggregate(
            f"C4P248_{index}_1" for index in indices
        )
        grouped_indicators[f"VSE1_{code}"] = binary_aggregate(
            f"C4P248_{index}_1_1" for index in indices
        )
        grouped_indicators[f"VSH_{code}"] = binary_aggregate(
            f"C4P248_{index}_3" for index in indices
        )
        grouped_indicators[f"VSH1_{code}"] = binary_aggregate(
            f"C4P248_{index}_3_1" for index in indices
        )
    for code, indices in cp_groups.items():
        grouped_indicators[f"VS_{code}"] = binary_aggregate(
            f"P248_{index:02d}_12M" for index in indices
        )
        grouped_indicators[f"VS1_{code}"] = binary_aggregate(
            f"C4P248_{index}" for index in indices
        )
        grouped_indicators[f"VSE_{code}"] = binary_aggregate(
            f"C4P248_{index}_1" for index in indices
        )
        grouped_indicators[f"VSE1_{code}"] = binary_aggregate(
            f"C4P248_{index}_1_1" for index in indices
        )
        grouped_indicators[f"VSH_{code}"] = binary_aggregate(
            f"C4P248_{index}_3" for index in indices
        )
        grouped_indicators[f"VSH1_{code}"] = binary_aggregate(
            f"C4P248_{index}_3_1" for index in indices
        )

    contact_indicators = {
        "VS_ICVAC_CONTACTO": (
            "CASE WHEN VS_ICVAC_301 = 1 OR VS_ICVAC_302 = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "VS_ICVAC_CONTACTO_VIDA": (
            "CASE WHEN VS_ICVAC_301_VIDA = 1 OR VS_ICVAC_302_VIDA = 1 "
            "THEN 1 ELSE 0 END"
        ),
    }

    aggressor_codes = {
        1: list(range(1, 18)),
        2: [1, 3, 5, 7, 9, 11, 13, 15],
        3: [2, 4, 6, 8, 10, 12, 14, 16],
        4: [17],
        5: [27, 28],
        6: [25],
        7: [26],
        8: [22, 23, 24],
        9: [18, 19, 20, 21],
    }
    aggressors: dict[str, str] = {}
    for group, codes in aggressor_codes.items():
        recent_hits = []
        life_hits = []
        for index in range(1, 17):
            who = " OR ".join(
                f"C4P248A_{code}_{index} = 1" for code in codes
            )
            recent_hits.append(
                f"(C4P248_{index} = 1 AND C4P248C_{index} = 1 "
                f"AND ({who}))"
            )
            life_hits.append(f"(C4P248_{index} = 1 AND ({who}))")
        aggressors[f"AG_VS12_{group:02d}"] = (
            "CASE WHEN " + " OR ".join(recent_hits) + " THEN 1 ELSE 0 END"
        )
        aggressors[f"AG_VSVIDA_{group:02d}"] = (
            "CASE WHEN " + " OR ".join(life_hits) + " THEN 1 ELSE 0 END"
        )

    raw_inputs.add("C4P248_O_12")
    for index in range(1, 17):
        raw_inputs.add(f"C4P248B_{index}")
    non_partner_recent = [
        f"(C4P248_{index} = 1 AND C4P248A_26_{index} != 1 "
        f"AND C4P248C_{index} = 1)"
        for index in range(1, 17)
    ]
    harassment_indices = [1, 2, 3, 4, 6, 7, 9, 13, 14]
    harassment_recent = [
        f"(C4P248_{index} = 1 AND C4P248A_26_{index} != 1 "
        f"AND C4P248C_{index} = 1)"
        for index in harassment_indices
    ]
    harassment_recent.append(
        '(UPPER(TRIM(CAST(C4P248_O_12 AS STRING))) = "ACOSO SEXUAL" '
        "AND C4P248A_26_12 != 1 AND C4P248C_12 = 1)"
    )
    before_twelve = [
        f"(C4P248_{index} = 1 AND C4P248B_{index} < 12)"
        for index in range(1, 17)
    ]
    women_indicators = {
        "INDICADOR_8_2_7": (
            "CASE WHEN SEXO = 1 AND ("
            + " OR ".join(non_partner_recent)
            + ") THEN 1 ELSE 0 END"
        ),
        "INDICADOR_8_2_13": (
            "CASE WHEN SEXO = 1 AND ("
            + " OR ".join(harassment_recent)
            + ") THEN 1 ELSE 0 END"
        ),
        "INDICADOR_8_2_8": (
            "CASE WHEN SEXO = 1 AND ("
            + " OR ".join(before_twelve)
            + ") THEN 1 ELSE 0 END"
        ),
    }

    aliases: dict[str, str] = {}
    for index in range(1, 17):
        aliases[f"Formas_VS_12M__C4P248_{index}"] = f"P248_{index:02d}_12M"
        aliases[f"Formas_VS_VIDA__C4P248_{index}"] = (
            f"CASE WHEN C4P248_{index} = 1 THEN 1 ELSE 0 END"
        )
        aliases[f"Formas_VS_E__C4P248_{index}"] = f"C4P248_{index}_1"
        aliases[f"Formas_VS_E_1__C4P248_{index}"] = f"C4P248_{index}_1_1"
        if index != 12:
            aliases[f"Formas_Agresor_VS_H__C4P248_{index}"] = (
                f"C4P248_{index}_3"
            )
            aliases[f"Formas_Agresor_VS_H_1__C4P248_{index}"] = (
                f"C4P248_{index}_3_1"
            )
    for code in ["301", "302", "303", "309"]:
        aliases[f"Formas_VS_12M__ICVAC_{code}"] = f"VS_ICVAC_{code}"
        aliases[f"Formas_VS_VIDA__ICVAC_{code}"] = f"VS_ICVAC_{code}_VIDA"
        aliases[f"Formas_VS_E__ICVAC_{code}"] = f"VSE_{code}"
        aliases[f"Formas_VS_E_1__ICVAC_{code}"] = f"VSE1_{code}"
        if code != "309":
            aliases[f"Formas_Agresor_VS_H__ICVAC_{code}"] = f"VSH_{code}"
            aliases[f"Formas_Agresor_VS_H_1__ICVAC_{code}"] = f"VSH1_{code}"
    for index in range(1, 10):
        code = f"CP{index:02d}"
        aliases[f"Formas_VS_12M__VS_{code}"] = f"VS_{code}"
        aliases[f"Formas_VS_VIDA__VS_{code}"] = f"VS1_{code}"
        aliases[f"Formas_VS_E__VSE_{code}"] = f"VSE_{code}"
        aliases[f"Formas_VS_E_1__VSE_{code}"] = f"VSE1_{code}"
        if index <= 8:
            aliases[f"Formas_Agresor_VS_H__VSH_{code}"] = f"VSH_{code}"
            aliases[f"Formas_Agresor_VS_H_1__VSH_{code}"] = f"VSH1_{code}"
    for index in range(1, 9):
        aliases[f"Agresor_VP_E__AG_VP_{index:02d}"] = f"AG_VP_E_{index:02d}"
        aliases[f"Agresor_VF_E__AG_VF_{index:02d}"] = f"AG_VF_E_{index:02d}"
        aliases[f"Agresor_VP_H__AG_VP_{index:02d}"] = f"AG_VP_H_{index:02d}"
        aliases[f"Agresor_VF_H__AG_VF_{index:02d}"] = f"AG_VF_H_{index:02d}"
    aliases["AG_VP_09"] = "AG_VP_E_09"
    aliases["AG_VF_09"] = "AG_VF_E_09"
    for index in range(1, 10):
        aliases[f"Agresor_VS_12M__AG_{index:02d}"] = f"AG_VS12_{index:02d}"
        aliases[f"Agresor_VS_VIDA__AG_{index:02d}"] = f"AG_VSVIDA_{index:02d}"
        prevalence_source = "AG_VSVIDA" if index <= 7 else "AG_VS12"
        aliases[f"Prev_Agresor_VS__AG_{index:02d}"] = (
            f"{prevalence_source}_{index:02d}"
        )
    for published, group in [("AG01", "02"), ("AG02", "03"), ("AG03", "04")]:
        aliases[f"Formas_Agresor_VS_H__VSH_{published}"] = f"AG_VS12_{group}"
        aliases[f"Formas_Agresor_VS_H_1__VSH_{published}"] = (
            f"AG_VSVIDA_{group}"
        )
    aliases["VS_OtraPersona_12M"] = "AG_VS12_06"
    aliases["VS_OtraPersona_VIDA"] = "AG_VSVIDA_06"

    blocks = [
        ("34_vs_formas_contexto", forms),
        ("34_vs_principales", main_indicators),
        ("34_vs_icvac_cp", grouped_indicators),
        ("34_vs_contacto", contact_indicators),
        ("34_vs_agresores", aggressors),
        ("34_vs_indicadores_mujeres", women_indicators),
        ("34_aliases_spss", aliases),
    ]
    return raw_inputs, blocks


def output_columns(blocks: list[tuple[str, dict[str, str]]]) -> list[str]:
    return [column for _, expressions in blocks for column in expressions]


def render_model() -> str:
    raw_inputs, blocks = build_stage34_contract()
    raw_only = sorted(set(raw_inputs) - set(KEY_DESIGN_COLUMNS))
    base_columns = KEY_DESIGN_COLUMNS + raw_only
    base_select = [f"    cleaned.`{column}`" for column in base_columns]
    base_select.extend(
        f"    household.`{column}` AS `{column}`"
        for column in HOUSEHOLD_DEPENDENCIES
    )
    base_select.extend(
        f"    school.`{column}` AS `{column}`"
        for column in SCHOOL_DEPENDENCIES
    )

    ctes = [
        "base AS (\n"
        "  SELECT\n"
        + ",\n".join(base_select)
        + "\n"
        '  FROM ${ref("cleaned_crs04_merged_adolescents_v0_5")} AS cleaned\n'
        '  LEFT JOIN ${ref("analytical_crs04_stage32_v0_5")} AS household\n'
        "    USING (ID, COLEGIAL_ID)\n"
        '  LEFT JOIN ${ref("analytical_crs04_stage33_v0_5")} AS school\n'
        "    USING (ID, COLEGIAL_ID)\n"
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
  name: "analytical_crs04_stage34_v0_5",
  description: "Stage 03 section 3.4 SPSS-authority shadow model.",
  tags: ["stage03", "analytical", "stage34", "shadow"]
}}

WITH
{",\n\n".join(ctes)}

SELECT
{final_select}
FROM {previous}
'''


def render_quality_assertion() -> str:
    _, blocks = build_stage34_contract()
    binary_condition = "\n    OR ".join(
        f"`{column}` NOT IN (0, 1) OR `{column}` IS NULL"
        for column in output_columns(blocks)
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage34", "quality"]
}}

WITH
candidate AS (
  SELECT *
  FROM ${{ref("analytical_crs04_stage34_v0_5")}}
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
    _, blocks = build_stage34_contract()
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
  tags: ["stage03", "analytical", "stage34", "parity"]
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
  FROM ${{ref("analytical_crs04_stage34_v0_5")}}
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
    _, blocks = build_stage34_contract()
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
