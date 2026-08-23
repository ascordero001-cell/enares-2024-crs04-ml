"""Generate the complete Stage 03 section 3.5 shadow model and assertions."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


MODEL_OUTPUT = Path(
    "dataform/definitions/analytical/analytical_crs04_stage35_v0_5.sqlx"
)
QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage35_shadow_quality.sqlx"
)
PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage35_shadow_v0_parity.sqlx"
)
KEY_DESIGN_COLUMNS = [
    "ID",
    "COLEGIAL_ID",
    "FACTOR_ALUMNOS",
    "CCDD",
    "SEXO",
    "AREA",
]
DEPENDENCIES = {
    "household": ["VP_HOGAR", "VF_HOGAR", "VP_o_VF_HOGAR"],
    "school": ["VP_ESCUELA", "VF_ESCUELA"],
    "sexual": ["VS_E", "VS_H", "VS_12M"],
}


def any_one(names: Iterable[str]) -> str:
    return "(" + " OR ".join(f"`{name}` = 1" for name in names) + ")"


def build_stage35_contract() -> tuple[set[str], list[tuple[str, dict[str, str]]]]:
    """Return raw inputs and the eight ordered SPSS 3.5 expression blocks."""

    raw_inputs = {
        "C3P233A",
        *(f"C3P233_{suffix}" for suffix in ["1", "1A", "2", "2A", "3"]),
        *(f"C3P231_{index}" for index in range(1, 7)),
        *(f"C3P231_{index}E{period}" for index in range(1, 6) for period in range(1, 5)),
        *(f"C3P243_{index}" for index in range(1, 7)),
        *(f"C3P243_T{index}" for index in range(1, 7)),
    }

    context: dict[str, str] = {}
    for suffix in ["1", "1A", "2", "2A", "3"]:
        context[f"C3P233_{suffix}_1"] = (
            f"CASE WHEN C3P233_{suffix} = 1 AND C3P233A = 1 "
            "THEN 1 ELSE 0 END"
        )
    for name, index in [
        ("LugarSalon_ViolEsc", 1),
        ("LugarPatio_ViolEsc", 2),
        ("LugarBano_ViolEsc", 3),
        ("LugarPasilloEscalera_ViolEsc", 4),
        ("LugarOtro_ViolEsc", 5),
        ("LugarFueraColegio_ViolEsc", 6),
    ]:
        context[name] = (
            f"CASE WHEN C3P231_{index} = 1 THEN 1 ELSE 0 END"
        )
    for name, period in [
        ("HoraEntrada_ViolEsc", 1),
        ("HoraClase_ViolEsc", 2),
        ("HoraRecreo_ViolEsc", 3),
        ("HoraSalida_ViolEsc", 4),
    ]:
        context[name] = (
            "CASE WHEN "
            + any_one(
                f"C3P231_{index}E{period}" for index in range(1, 6)
            )
            + " THEN 1 ELSE 0 END"
        )

    exercised = {
        "VP_EJERCIDA": (
            "CASE WHEN "
            + any_one(["C3P233_2_1", "C3P233_2A_1", "C3P233_3_1"])
            + " THEN 1 ELSE 0 END"
        ),
        "VF_EJERCIDA": (
            "CASE WHEN "
            + any_one(["C3P233_1_1", "C3P233_1A_1"])
            + " THEN 1 ELSE 0 END"
        ),
    }
    school_combinations = {
        "VP_o_VF_E": (
            "CASE WHEN VP_ESCUELA = 1 OR VF_ESCUELA = 1 THEN 1 ELSE 0 END"
        ),
        "VP_VF_E": (
            "CASE WHEN VP_ESCUELA = 1 AND VF_ESCUELA = 1 THEN 1 ELSE 0 END"
        ),
        "VP_VF_VS_E": (
            "CASE WHEN VP_ESCUELA = 1 AND VF_ESCUELA = 1 AND VS_E = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "VP_o_VF_EJERCIDA": (
            "CASE WHEN VP_EJERCIDA = 1 OR VF_EJERCIDA = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "INDICADOR_8_3_9": (
            "CASE WHEN VP_ESCUELA = 1 OR VF_ESCUELA = 1 OR VS_E = 1 "
            "THEN 1 ELSE 0 END"
        ),
    }
    school_aliases = {
        "VP_o_VF_ESCUELA": "VP_o_VF_E",
        "Solap_VP_VF_E__Coexistencia": "VP_VF_E",
    }
    household_three_forms = {
        "VS_HOGAR": "VS_H",
        "VP_VF_VS_HOGAR": (
            "CASE WHEN VP_HOGAR = 1 AND VF_HOGAR = 1 AND VS_H = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "VP_o_VF_o_VS_HOGAR": (
            "CASE WHEN VP_HOGAR = 1 OR VF_HOGAR = 1 OR VS_H = 1 "
            "THEN 1 ELSE 0 END"
        ),
    }
    accumulation = {
        "PV_hogar_escuela1": (
            "CASE WHEN VP_o_VF_o_VS_HOGAR = 1 AND INDICADOR_8_3_9 = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "PV_hogar_escuela": (
            "CASE WHEN VP_o_VF_HOGAR = 1 AND VP_o_VF_E = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "PV_VP_hogar_escuela": (
            "CASE WHEN VP_HOGAR = 1 AND VP_ESCUELA = 1 THEN 1 ELSE 0 END"
        ),
        "PV_VF_hogar_escuela": (
            "CASE WHEN VF_HOGAR = 1 AND VF_ESCUELA = 1 THEN 1 ELSE 0 END"
        ),
        "PV_VP_hogar_VF_escuela": (
            "CASE WHEN VP_HOGAR = 1 AND VF_ESCUELA = 1 THEN 1 ELSE 0 END"
        ),
        "PV_VF_hogar_VP_escuela": (
            "CASE WHEN VF_HOGAR = 1 AND VP_ESCUELA = 1 THEN 1 ELSE 0 END"
        ),
        "PV_VP_VF_hogar_escuela": (
            "CASE WHEN VP_HOGAR = 1 AND VF_HOGAR = 1 "
            "AND VP_ESCUELA = 1 AND VF_ESCUELA = 1 THEN 1 ELSE 0 END"
        ),
        "PV_VP_VF_hogar_escuela_VS": (
            "CASE WHEN VP_HOGAR = 1 AND VF_HOGAR = 1 "
            "AND VP_ESCUELA = 1 AND VF_ESCUELA = 1 AND VS_12M = 1 "
            "THEN 1 ELSE 0 END"
        ),
        "PV_indice_acum": (
            "COALESCE(VP_HOGAR, 0) + COALESCE(VF_HOGAR, 0) "
            "+ COALESCE(VP_ESCUELA, 0) + COALESCE(VF_ESCUELA, 0)"
        ),
        "PV_indice_acum_VS": (
            "COALESCE(VP_HOGAR, 0) + COALESCE(VF_HOGAR, 0) "
            "+ COALESCE(VP_ESCUELA, 0) + COALESCE(VF_ESCUELA, 0) "
            "+ COALESCE(VS_12M, 0)"
        ),
    }

    consequence_items = [f"C3P243_{index}" for index in range(1, 7)]
    consequence_health = [f"C3P243_T{index}" for index in range(1, 7)]
    valid = " AND ".join(f"{name} IS NOT NULL" for name in consequence_items)
    count = " + ".join(
        f"CASE WHEN {name} = 1 THEN 1 ELSE 0 END"
        for name in consequence_items
    )
    consequence_base = {
        "CONS_ALGUNA": (
            f"CASE WHEN NOT ({valid}) THEN NULL WHEN "
            + any_one(consequence_items)
            + " THEN 1 ELSE 0 END"
        ),
        "CONS_NUM_CONSECUENCIAS": (
            f"CASE WHEN NOT ({valid}) THEN NULL ELSE {count} END"
        ),
    }
    consequence_care = {
        "CONS_ATENCION_SALUD": (
            "CASE WHEN CONS_ALGUNA != 1 OR CONS_ALGUNA IS NULL THEN NULL "
            "WHEN "
            + any_one(consequence_health)
            + " THEN 1 ELSE 0 END"
        )
    }

    blocks = [
        ("336_escuela_contexto", context),
        ("336_escuela_ejercida", exercised),
        ("33_escuela_combinaciones", school_combinations),
        ("33_escuela_aliases_publicados", school_aliases),
        ("32_hogar_tres_formas", household_three_forms),
        ("35_acumulacion", accumulation),
        ("354_consecuencias_base", consequence_base),
        ("354_consecuencias_salud", consequence_care),
    ]
    return raw_inputs, blocks


def output_columns(blocks: list[tuple[str, dict[str, str]]]) -> list[str]:
    return [column for _, expressions in blocks for column in expressions]


def binary_non_null_columns(
    blocks: list[tuple[str, dict[str, str]]],
) -> list[str]:
    excluded = {
        "PV_indice_acum",
        "PV_indice_acum_VS",
        "CONS_ALGUNA",
        "CONS_NUM_CONSECUENCIAS",
        "CONS_ATENCION_SALUD",
    }
    return [column for column in output_columns(blocks) if column not in excluded]


def render_model() -> str:
    raw_inputs, blocks = build_stage35_contract()
    raw_only = sorted(set(raw_inputs) - set(KEY_DESIGN_COLUMNS))
    base_select = [
        *(f"    cleaned.`{column}`" for column in KEY_DESIGN_COLUMNS + raw_only),
        *(f"    household.`{column}` AS `{column}`" for column in DEPENDENCIES["household"]),
        *(f"    school.`{column}` AS `{column}`" for column in DEPENDENCIES["school"]),
        *(f"    sexual.`{column}` AS `{column}`" for column in DEPENDENCIES["sexual"]),
    ]
    ctes = [
        "base AS (\n  SELECT\n"
        + ",\n".join(base_select)
        + "\n"
        '  FROM ${ref("cleaned_crs04_merged_adolescents_v0_5")} AS cleaned\n'
        '  LEFT JOIN ${ref("analytical_crs04_stage32_v0_5")} AS household\n'
        "    USING (ID, COLEGIAL_ID)\n"
        '  LEFT JOIN ${ref("analytical_crs04_stage33_v0_5")} AS school\n'
        "    USING (ID, COLEGIAL_ID)\n"
        '  LEFT JOIN ${ref("analytical_crs04_stage34_v0_5")} AS sexual\n'
        "    USING (ID, COLEGIAL_ID)\n)"
    ]
    previous = "base"
    for index, (block_name, expressions) in enumerate(blocks, start=1):
        cte_name = f"block_{index:02d}_{block_name}"
        derived = ",\n".join(
            f"    {expression} AS `{column}`"
            for column, expression in expressions.items()
        )
        ctes.append(
            f"{cte_name} AS (\n  SELECT\n    *,\n{derived}\n"
            f"  FROM {previous}\n)"
        )
        previous = cte_name
    final_columns = KEY_DESIGN_COLUMNS + output_columns(blocks)
    final_select = ",\n".join(f"  `{column}`" for column in final_columns)
    return f'''config {{
  type: "table",
  schema: dataform.projectConfig.vars.analyticalDataset,
  name: "analytical_crs04_stage35_v0_5",
  description: "Stage 03 section 3.5 SPSS-authority shadow model.",
  tags: ["stage03", "analytical", "stage35", "shadow"]
}}

WITH
{",\n\n".join(ctes)}

SELECT
{final_select}
FROM {previous}
'''


def render_quality_assertion() -> str:
    _, blocks = build_stage35_contract()
    binary_condition = "\n    OR ".join(
        f"`{column}` NOT IN (0, 1) OR `{column}` IS NULL"
        for column in binary_non_null_columns(blocks)
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage35", "quality"]
}}

WITH
candidate AS (
  SELECT * FROM ${{ref("analytical_crs04_stage35_v0_5")}}
),
duplicate_keys AS (
  SELECT ID, COLEGIAL_ID FROM candidate
  GROUP BY ID, COLEGIAL_ID HAVING COUNT(*) > 1
),
checks AS (
  SELECT "row_count" AS check_name, ABS(COUNT(*) - 18807) AS violation_count
  FROM candidate HAVING COUNT(*) != 18807
  UNION ALL
  SELECT "null_keys", COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL)
  FROM candidate HAVING COUNTIF(ID IS NULL OR COLEGIAL_ID IS NULL) > 0
  UNION ALL
  SELECT "duplicate_key_groups", COUNT(*) FROM duplicate_keys HAVING COUNT(*) > 0
  UNION ALL
  SELECT "survey_design_fields", COUNTIF(
    FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0
    OR CCDD IS NULL OR SEXO IS NULL OR AREA IS NULL)
  FROM candidate HAVING COUNTIF(
    FACTOR_ALUMNOS IS NULL OR FACTOR_ALUMNOS <= 0
    OR CCDD IS NULL OR SEXO IS NULL OR AREA IS NULL) > 0
  UNION ALL
  SELECT "binary_outputs", COUNTIF({binary_condition})
  FROM candidate HAVING COUNTIF({binary_condition}) > 0
  UNION ALL
  SELECT "accumulation_ranges", COUNTIF(
    PV_indice_acum NOT BETWEEN 0 AND 4
    OR PV_indice_acum_VS NOT BETWEEN 0 AND 5)
  FROM candidate HAVING COUNTIF(
    PV_indice_acum NOT BETWEEN 0 AND 4
    OR PV_indice_acum_VS NOT BETWEEN 0 AND 5) > 0
  UNION ALL
  SELECT "consequence_ranges", COUNTIF(
    CONS_ALGUNA NOT IN (0, 1)
    OR CONS_NUM_CONSECUENCIAS NOT BETWEEN 0 AND 6
    OR CONS_ATENCION_SALUD NOT IN (0, 1))
  FROM candidate HAVING COUNTIF(
    CONS_ALGUNA NOT IN (0, 1)
    OR CONS_NUM_CONSECUENCIAS NOT BETWEEN 0 AND 6
    OR CONS_ATENCION_SALUD NOT IN (0, 1)) > 0
)
SELECT * FROM checks
'''


def render_parity_assertion() -> str:
    _, blocks = build_stage35_contract()
    columns = output_columns(blocks)
    selected = ",\n".join(f"    `{column}`" for column in columns)
    comparisons = "\n  OR ".join(
        f"candidate.`{column}` IS DISTINCT FROM reference.`{column}`"
        for column in columns
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage35", "parity"]
}}

WITH
reference AS (
  SELECT CAST(ID AS INT64) AS ID, CAST(COLEGIAL_ID AS INT64) AS COLEGIAL_ID,
{selected}
  FROM ${{ref("analytical_crs04_adolescents")}}
),
candidate AS (
  SELECT ID, COLEGIAL_ID,
{selected}
  FROM ${{ref("analytical_crs04_stage35_v0_5")}}
)
SELECT COALESCE(candidate.ID, reference.ID) AS ID,
  COALESCE(candidate.COLEGIAL_ID, reference.COLEGIAL_ID) AS COLEGIAL_ID
FROM candidate FULL OUTER JOIN reference USING (ID, COLEGIAL_ID)
WHERE candidate.ID IS NULL OR reference.ID IS NULL OR {comparisons}
'''


def main() -> None:
    _, blocks = build_stage35_contract()
    for path, content in [
        (MODEL_OUTPUT, render_model()),
        (QUALITY_OUTPUT, render_quality_assertion()),
        (PARITY_OUTPUT, render_parity_assertion()),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8", newline="\n")
        print(f"Generated: {path}")
    print(f"Blocks generated: {len(blocks)}")
    print(f"Derived columns generated: {len(output_columns(blocks))}")


if __name__ == "__main__":
    main()
