"""Generate the complete Stage 03 section 3.6 shadow model and assertions."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


MODEL_OUTPUT = Path(
    "dataform/definitions/analytical/analytical_crs04_stage36_v0_5.sqlx"
)
QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage36_shadow_quality.sqlx"
)
PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage36_shadow_v0_parity.sqlx"
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
    "household": ["VP_HOGAR", "VF_HOGAR"],
    "school": ["VP_ESCUELA", "VF_ESCUELA"],
    "sexual": ["VS_12M"],
}
PEOPLE = {
    "madre": [1],
    "padre": [2],
    "madrastra": [3],
    "padrastro": [4],
    "hermana": [5],
    "hermano": [6],
    "abuela": [7],
    "abuelo": [8],
    "tia": [9],
    "tio": [10],
    "otro_pariente": [11],
    "familiar": list(range(1, 12)),
    "car": [12, 13, 14],
    "escolar_adulto": [15, 16, 17, 18],
    "pares_amigos": [19, 20],
    "otro": [21],
}


def any_one(names: Iterable[str]) -> str:
    return "(" + " OR ".join(f"`{name}` = 1" for name in names) + ")"


def recode_12(source: str) -> str:
    return f"CASE WHEN {source} = 1 THEN 1 WHEN {source} = 2 THEN 0 END"


def build_stage36_contract() -> tuple[set[str], list[tuple[str, dict[str, str]]]]:
    """Return raw inputs and the four ordered SPSS 3.6 expression blocks."""

    raw_inputs: set[str] = set()
    help_components: dict[str, str] = {}
    contexts = [
        (
            "hogar",
            "ayuda_hogar",
            "C3P209",
            "C3P210",
            "C3P211",
            "C3P212",
            "C3P214",
            [
                "consuelo",
                "consejo",
                "hablo_familia",
                "llamo_atencion",
                "respuesta_agresion",
                "otro_tipo",
            ],
        ),
        (
            "escuela",
            "ayuda_escuela",
            "C3P236",
            "C3P237",
            "C3P238",
            "C3P239",
            "C3P241",
            [
                "consuelo",
                "aviso_docente",
                "hablo_agresor",
                "llamo_atencion",
                "hablo_director",
                "hablo_padres_agresor",
                "consejo",
                "otro_tipo",
            ],
        ),
    ]
    for (
        context,
        prefix,
        search,
        people_question,
        received,
        response_question,
        institutional,
        responses,
    ) in contexts:
        raw_inputs.update({search, received, institutional})
        help_components[f"busco_ayuda_{context}"] = recode_12(search)
        help_components[f"recibio_ayuda_{context}"] = recode_12(received)
        help_components[f"apoyo_institucional_{context}"] = recode_12(
            institutional
        )
        for label, indices in PEOPLE.items():
            columns = [f"{people_question}_{index}" for index in indices]
            raw_inputs.update(columns)
            help_components[f"{prefix}_{label}"] = (
                f"CASE WHEN {search} IN (1,2) AND {any_one(columns)} THEN 1 "
                f"WHEN {search} IN (1,2) THEN 0 END"
            )
        for index, label in enumerate(responses, start=1):
            column = f"{response_question}_{index}"
            raw_inputs.add(column)
            help_components[f"{prefix}_{label}"] = (
                f"CASE WHEN {column} = 1 THEN 1 ELSE 0 END"
            )

    help_derived = {
        "recibio_ayuda_hogar_victimas": (
            "CASE WHEN (VP_HOGAR = 1 OR VF_HOGAR = 1) AND C3P211 = 3 "
            "THEN NULL WHEN VP_HOGAR = 1 OR VF_HOGAR = 1 "
            "THEN CASE WHEN C3P211 = 1 THEN 1 ELSE 0 END END"
        ),
        "brecha_ayuda_hogar": (
            "CASE WHEN busco_ayuda_hogar = 1 AND recibio_ayuda_hogar = 0 "
            "THEN 1 WHEN busco_ayuda_hogar = 1 "
            "AND recibio_ayuda_hogar = 1 THEN 0 END"
        ),
        "brecha_institucional_hogar": (
            "CASE WHEN (VP_HOGAR = 1 OR VF_HOGAR = 1) "
            "AND apoyo_institucional_hogar = 0 THEN 1 "
            "WHEN (VP_HOGAR = 1 OR VF_HOGAR = 1) "
            "AND apoyo_institucional_hogar = 1 THEN 0 END"
        ),
        "recibio_ayuda_escuela_victimas": (
            "CASE WHEN (VP_ESCUELA = 1 OR VF_ESCUELA = 1) "
            "AND C3P238 = 3 THEN NULL "
            "WHEN VP_ESCUELA = 1 OR VF_ESCUELA = 1 "
            "THEN CASE WHEN C3P238 = 1 THEN 1 ELSE 0 END END"
        ),
        "brecha_ayuda_escuela": (
            "CASE WHEN busco_ayuda_escuela = 1 "
            "AND recibio_ayuda_escuela = 0 THEN 1 "
            "WHEN busco_ayuda_escuela = 1 "
            "AND recibio_ayuda_escuela = 1 THEN 0 END"
        ),
        "brecha_institucional_escuela": (
            "CASE WHEN (VP_ESCUELA = 1 OR VF_ESCUELA = 1) "
            "AND apoyo_institucional_escuela = 0 THEN 1 "
            "WHEN (VP_ESCUELA = 1 OR VF_ESCUELA = 1) "
            "AND apoyo_institucional_escuela = 1 THEN 0 END"
        ),
    }

    raw_inputs.update({"C4P252", "C4P254", "C4P257", "C4P259", "C3P246", "C3P247"})
    sexual_components = {
        "busco_ayuda_vs": recode_12("C4P252"),
        "recibio_ayuda_vs": recode_12("C4P254"),
        "apoyo_institucional_vs": recode_12("C4P257"),
        "recibio_ayuda_institucional_vs": recode_12("C4P259"),
        "conoce_demuna": recode_12("C3P246"),
        "uso_demuna": recode_12("C3P247"),
    }
    for label, indices in PEOPLE.items():
        columns = [f"C4P253_{index}" for index in indices]
        raw_inputs.update(columns)
        sexual_components[f"ayuda_vs_{label}"] = (
            f"CASE WHEN C4P252 IN (1,2) AND {any_one(columns)} THEN 1 "
            "WHEN C4P252 IN (1,2) THEN 0 END"
        )
    for index, label in enumerate(
        [
            "consejo",
            "hablo_madre_padre",
            "reclamo_agresor",
            "aviso_autoridades",
            "refugio",
            "especialista",
            "otro_tipo",
        ],
        start=1,
    ):
        column = f"C4P255_{index}"
        raw_inputs.add(column)
        sexual_components[f"ayuda_vs_{label}"] = (
            f"CASE WHEN {column} = 1 THEN 1 ELSE 0 END"
        )
    for index, label in enumerate(
        ["hablo_familia", "terapias", "llamo_atencion", "otro"], start=1
    ):
        column = f"C4P260_{index}"
        raw_inputs.add(column)
        sexual_components[f"ayuda_inst_vs_{label}"] = (
            f"CASE WHEN {column} = 1 THEN 1 ELSE 0 END"
        )

    sexual_derived = {
        "recibio_ayuda_vs_victimas": (
            "CASE WHEN VS_12M = 1 AND C4P254 = 3 THEN NULL "
            "WHEN VS_12M = 1 THEN CASE WHEN C4P254 = 1 THEN 1 ELSE 0 END END"
        ),
        "brecha_ayuda_vs": (
            "CASE WHEN busco_ayuda_vs = 1 AND recibio_ayuda_vs = 0 THEN 1 "
            "WHEN busco_ayuda_vs = 1 AND recibio_ayuda_vs = 1 THEN 0 END"
        ),
        "brecha_institucional_vs": (
            "CASE WHEN VS_12M = 1 AND apoyo_institucional_vs = 0 THEN 1 "
            "WHEN VS_12M = 1 AND apoyo_institucional_vs = 1 THEN 0 END"
        ),
    }

    blocks = [
        ("36_ayuda_componentes", help_components),
        ("36_ayuda_derivados", help_derived),
        ("36_ayuda_vs_componentes", sexual_components),
        ("36_ayuda_vs_derivados", sexual_derived),
    ]
    return raw_inputs, blocks


def output_columns(blocks: list[tuple[str, dict[str, str]]]) -> list[str]:
    return [column for _, expressions in blocks for column in expressions]


def render_model() -> str:
    raw_inputs, blocks = build_stage36_contract()
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
  name: "analytical_crs04_stage36_v0_5",
  description: "Stage 03 section 3.6 SPSS-authority shadow model.",
  tags: ["stage03", "analytical", "stage36", "shadow"]
}}

WITH
{",\n\n".join(ctes)}

SELECT
{final_select}
FROM {previous}
'''


def render_quality_assertion() -> str:
    _, blocks = build_stage36_contract()
    domain_condition = "\n    OR ".join(
        f"`{column}` NOT IN (0, 1)" for column in output_columns(blocks)
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage36", "quality"]
}}

WITH
candidate AS (SELECT * FROM ${{ref("analytical_crs04_stage36_v0_5")}}),
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
  SELECT "binary_domains", COUNTIF({domain_condition})
  FROM candidate HAVING COUNTIF({domain_condition}) > 0
)
SELECT * FROM checks
'''


def render_parity_assertion() -> str:
    _, blocks = build_stage36_contract()
    columns = output_columns(blocks)
    selected = ",\n".join(f"    `{column}`" for column in columns)
    comparisons = "\n  OR ".join(
        f"candidate.`{column}` IS DISTINCT FROM reference.`{column}`"
        for column in columns
    )
    return f'''config {{
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage36", "parity"]
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
  FROM ${{ref("analytical_crs04_stage36_v0_5")}}
)
SELECT COALESCE(candidate.ID, reference.ID) AS ID,
  COALESCE(candidate.COLEGIAL_ID, reference.COLEGIAL_ID) AS COLEGIAL_ID
FROM candidate FULL OUTER JOIN reference USING (ID, COLEGIAL_ID)
WHERE candidate.ID IS NULL OR reference.ID IS NULL OR {comparisons}
'''


def main() -> None:
    _, blocks = build_stage36_contract()
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
