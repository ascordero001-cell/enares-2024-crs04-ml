"""Generate the Stage 03 section 3.1 shadow model and assertions.

The formulas are a direct transcription of the validated SPSS-authority
implementation in notebook 02.  Keeping them in one generator makes the
Dataform model reproducible and gives unit tests a pure contract to inspect.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


MODEL_OUTPUT = Path(
    "dataform/definitions/analytical/analytical_crs04_stage31_v0_5.sqlx"
)
QUALITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage31_shadow_quality.sqlx"
)
PARITY_OUTPUT = Path(
    "dataform/definitions/assertions/stage31_shadow_v0_parity.sqlx"
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


def coalesce_sum(names: Iterable[str]) -> str:
    return " + ".join(f"COALESCE(`{name}`, 0)" for name in names)


def build_stage31_contract() -> tuple[set[str], list[tuple[str, dict[str, str]]]]:
    """Return raw inputs and the ten ordered SPSS 3.1 expression blocks."""

    factor_required = {
        "C4P129",
        "C3P128",
        "C3P105",
        "C3P126",
        "C3P127",
        "C3P123",
        "C3P218",
        "C3P219",
        "C3P220",
        "C3P122",
        "CCDD",
        "CCPP",
        "SEXO",
        *(f"C4P130_{index}" for index in range(1, 7)),
        *(f"C3P115_{index}" for index in range(1, 5)),
        *(f"C3P216A_{index}" for index in range(1, 7)),
        *(f"C3P216A_{index}C" for index in range(1, 7)),
        *(f"C3P216C_{index}" for index in range(1, 6)),
        *(f"C3P216C_{index}C" for index in range(1, 6)),
    }

    parent_missing = " OR ".join(
        f"C3P115_{index} IS NULL" for index in range(1, 5)
    )
    biparental = " OR ".join(
        [
            "(C3P115_1 = 1 AND C3P115_2 = 1)",
            "(C3P115_1 = 1 AND C3P115_4 = 1)",
            "(C3P115_2 = 1 AND C3P115_3 = 1)",
            "(C3P115_3 = 1 AND C3P115_4 = 1)",
        ]
    )
    monoparental = " OR ".join(
        f"(C3P115_{index} = 1 AND "
        + " AND ".join(
            f"C3P115_{other} != 1"
            for other in range(1, 5)
            if other != index
        )
        + ")"
        for index in range(1, 5)
    )
    personal_hit = " OR ".join(
        f"(C3P216A_{index} = 1 AND C3P216A_{index}C = 1)"
        for index in range(1, 7)
    )
    induced_hit = " OR ".join(
        f"(C3P216C_{index} = 1 AND C3P216C_{index}C = 1)"
        for index in range(1, 6)
    )

    factors = {
        "etnicidad1": """CASE
          WHEN C4P129 IN (1, 2) THEN 1
          WHEN C4P129 IN (3, 4) THEN 3
          WHEN C4P129 = 5 THEN 5
          WHEN C4P129 IN (6, 7, 8) THEN 6
          WHEN C4P129 = 9 THEN 9
        END""",
        "idiomaHogar": """CASE
          WHEN C3P128 IS NULL THEN -1
          WHEN C3P128 = 1 THEN 1
          WHEN C3P128 IN (2, 3) THEN 3
          WHEN C3P128 = 4 THEN 4
        END""",
        "DISCAPACIDAD": """CASE
          WHEN C4P130_1 = 1 OR C4P130_2 = 1 OR C4P130_3 = 1
            OR C4P130_4 = 1 OR C4P130_5 = 1 OR C4P130_6 = 1 THEN 1
          WHEN C4P130_1 = 2 AND C4P130_2 = 2 AND C4P130_3 = 2
            AND C4P130_4 = 2 AND C4P130_5 = 2 AND C4P130_6 = 2 THEN 0
        END""",
        "tipo_hogar1": f"""CASE
          WHEN C3P105 = 2 THEN 3
          WHEN C3P105 != 2 AND ({biparental}) THEN 1
          WHEN C3P105 != 2 AND ({monoparental}) THEN 2
          WHEN {parent_missing} THEN -1
          ELSE 3
        END""",
        "DEPARTAMENTO2": """CASE
          WHEN LPAD(CAST(CCDD AS STRING), 2, '0') = '15'
            AND LPAD(CAST(CCPP AS STRING), 2, '0')
              IN ('02','03','04','05','06','07','08','09','10') THEN '64'
          ELSE LPAD(CAST(CCDD AS STRING), 2, '0')
        END""",
        "OPINION_TOMADA": """CASE
          WHEN C3P126 = 2 THEN 0
          WHEN C3P126 = 1 AND C3P127 = 2 THEN 1
          WHEN C3P126 = 1 AND C3P127 = 1 THEN 0
          ELSE -1
        END""",
        "discusion_hogar": (
            "CASE WHEN C3P123 = 1 THEN 1 WHEN C3P123 = 2 THEN 0 END"
        ),
        "Desemp_DesaproboCurso": (
            "CASE WHEN C3P218 = 1 THEN 1 WHEN C3P218 = 2 THEN 0 END"
        ),
        "Desemp_RepitioGrado": (
            "CASE WHEN C3P219 = 1 THEN 1 WHEN C3P219 = 2 THEN 0 END"
        ),
        "Desemp_ExpulsionColegio": (
            "CASE WHEN C3P220 = 1 THEN 1 WHEN C3P220 = 2 THEN 0 END"
        ),
        "conducta_riesgo_personal": (
            f"CASE WHEN SEXO IN (1, 2) AND ({personal_hit}) THEN 1 ELSE 0 END"
        ),
        "conducta_riesgo_inducido": (
            f"CASE WHEN SEXO IN (1, 2) AND ({induced_hit}) THEN 1 ELSE 0 END"
        ),
        "no_ir_colegio": "CASE WHEN C3P122 = 1 THEN 1 ELSE 0 END",
    }

    risk_total = {
        "riesgo_total": """CASE
          WHEN conducta_riesgo_personal = 1 OR conducta_riesgo_inducido = 1
            THEN 1
          ELSE 0
        END"""
    }

    attitude_required = {f"C3P301_{index}" for index in range(1, 7)}
    attitudes = {
        "justifica_castigo_docente": (
            "CASE WHEN C3P301_4 = 1 THEN 1 WHEN C3P301_4 = 2 THEN 0 END"
        ),
        "justifica_castigo_parental": (
            "CASE WHEN C3P301_5 = 1 THEN 1 WHEN C3P301_5 = 2 THEN 0 END"
        ),
        "reconoce_derecho_opinar": (
            "CASE WHEN C3P301_2 = 1 THEN 1 WHEN C3P301_2 = 2 THEN 0 END"
        ),
        "reconoce_derecho_denunciar": (
            "CASE WHEN C3P301_6 = 1 THEN 1 WHEN C3P301_6 = 2 THEN 0 END"
        ),
        "rechaza_dejar_estudiar": (
            "CASE WHEN C3P301_3 = 1 THEN 0 WHEN C3P301_3 = 2 THEN 1 END"
        ),
        "rechaza_trabajo_infantil_necesidad": (
            "CASE WHEN C3P301_1 = 1 THEN 0 WHEN C3P301_1 = 2 THEN 1 END"
        ),
    }
    rights = [
        "reconoce_derecho_opinar",
        "reconoce_derecho_denunciar",
        "rechaza_dejar_estudiar",
        "rechaza_trabajo_infantil_necesidad",
    ]
    rights_sum = coalesce_sum(rights)
    aggregates = {
        "justifica_al_menos_una": """CASE
          WHEN justifica_castigo_docente IS NULL
            AND justifica_castigo_parental IS NULL THEN NULL
          ELSE GREATEST(
            COALESCE(justifica_castigo_docente, 0),
            COALESCE(justifica_castigo_parental, 0)
          )
        END""",
        "n_formas_justificadas": """CASE
          WHEN justifica_castigo_docente IS NULL
            AND justifica_castigo_parental IS NULL THEN NULL
          ELSE COALESCE(justifica_castigo_docente, 0)
            + COALESCE(justifica_castigo_parental, 0)
        END""",
        "indice_derechos": (
            "CASE WHEN "
            + " AND ".join(f"{name} IS NULL" for name in rights)
            + f" THEN NULL ELSE {rights_sum} END"
        ),
        "reconoce_todos_derechos_clave": (
            "CASE WHEN "
            + " OR ".join(f"{name} IS NULL" for name in rights)
            + " THEN NULL WHEN "
            + " AND ".join(f"{name} = 1" for name in rights)
            + " THEN 1 ELSE 0 END"
        ),
    }
    rights_threshold = {
        "reconoce_3omas_derechos": """CASE
          WHEN indice_derechos IS NULL THEN NULL
          WHEN indice_derechos >= 3 THEN 1
          ELSE 0
        END"""
    }

    task_required = {f"C3P302_{index}" for index in range(1, 11)}
    task_components: dict[str, str] = {}
    for index in range(1, 8):
        source = f"C3P302_{index}"
        task_components[f"tarea{index}_fem"] = (
            f"CASE WHEN {source} IN (2,4,6) THEN 1 "
            f"WHEN {source} IN (1,3,5,7) THEN 0 END"
        )
        task_components[f"tarea{index}_masc"] = (
            f"CASE WHEN {source} IN (3,5,7) THEN 1 "
            f"WHEN {source} IN (1,2,4,6) THEN 0 END"
        )
        task_components[f"tarea{index}_nna"] = (
            f"CASE WHEN {source} = 1 THEN 1 "
            f"WHEN {source} IN (2,3,4,5,6,7) THEN 0 END"
        )
    for index in range(8, 11):
        source = f"C3P302_{index}"
        task_components[f"tarea{index}_fem"] = (
            f"CASE WHEN {source} IN (2,4,6) THEN 1 "
            f"WHEN {source} IN (3,5,7,8) THEN 0 END"
        )
        task_components[f"tarea{index}_masc"] = (
            f"CASE WHEN {source} IN (3,5,7) THEN 1 "
            f"WHEN {source} IN (2,4,6,8) THEN 0 END"
        )
        task_components[f"tarea{index}_nadie"] = (
            f"CASE WHEN {source} = 8 THEN 1 "
            f"WHEN {source} IN (2,3,4,5,6,7) THEN 0 END"
        )

    feminine = [f"tarea{index}_fem" for index in range(1, 11)]
    masculine = [f"tarea{index}_masc" for index in range(1, 11)]
    children = [f"tarea{index}_nna" for index in range(1, 8)]
    nobody = [f"tarea{index}_nadie" for index in range(8, 11)]
    valid_1_7 = " + ".join(
        f"CASE WHEN C3P302_{index} IN (1,2,3,4,5,6,7) THEN 1 ELSE 0 END"
        for index in range(1, 8)
    )
    valid_8_10 = " + ".join(
        f"CASE WHEN C3P302_{index} IN (2,3,4,5,6,7,8) THEN 1 ELSE 0 END"
        for index in range(8, 11)
    )
    task_counts = {
        "n_tareas_femeninas": coalesce_sum(feminine),
        "n_tareas_masculinas": coalesce_sum(masculine),
        "n_tareas_nna": coalesce_sum(children),
        "n_tareas_nadie": coalesce_sum(nobody),
        "n_tareas_validas_1_7": valid_1_7,
        "n_tareas_validas_8_10": valid_8_10,
        "n_tareas_validas_p302": f"({valid_1_7}) + ({valid_8_10})",
    }
    task_indicators = {
        "prop_tareas_femeninas": (
            "SAFE_DIVIDE(n_tareas_femeninas, n_tareas_validas_p302)"
        ),
        "prop_tareas_masculinas": (
            "SAFE_DIVIDE(n_tareas_masculinas, n_tareas_validas_p302)"
        ),
        "predominio_femenino_tareas": """CASE
          WHEN n_tareas_validas_p302 = 0 THEN NULL
          WHEN n_tareas_femeninas > n_tareas_masculinas THEN 1
          ELSE 0
        END""",
    }

    myth_map = {
        "mito_locas": "C3P303_1",
        "mito_pobreza": "C3P303_3",
        "mito_fuera_casa": "C3P303_4",
        "mito_sitios_oscuros": "C3P303_5",
    }
    myths = {
        name: f"CASE WHEN {source} = 1 THEN 1 WHEN {source} = 2 THEN 0 END"
        for name, source in myth_map.items()
    }
    myth_names = list(myth_map)
    myth_sum = coalesce_sum(myth_names)
    myth_all_missing = " AND ".join(
        f"{name} IS NULL" for name in myth_names
    )
    myth_aggregates = {
        "n_mitos": (
            f"CASE WHEN {myth_all_missing} THEN NULL ELSE {myth_sum} END"
        ),
        "cree_al_menos_un_mito": (
            f"CASE WHEN {myth_all_missing} THEN NULL WHEN "
            + " OR ".join(f"{name} = 1" for name in myth_names)
            + " THEN 1 ELSE 0 END"
        ),
    }

    raw_inputs = factor_required | attitude_required | task_required | set(
        myth_map.values()
    )
    blocks = [
        ("31_factores", factors),
        ("31_riesgo_total", risk_total),
        ("31_actitudes_componentes", attitudes),
        ("31_actitudes_agregados", aggregates),
        ("31_reconoce_tres_mas", rights_threshold),
        ("31_tareas_componentes", task_components),
        ("31_tareas_conteos", task_counts),
        ("31_tareas_indicador", task_indicators),
        ("31_mitos_componentes", myths),
        ("31_mitos_agregados", myth_aggregates),
    ]
    return raw_inputs, blocks


def output_columns(blocks: list[tuple[str, dict[str, str]]]) -> list[str]:
    return [column for _, expressions in blocks for column in expressions]


def render_model() -> str:
    raw_inputs, blocks = build_stage31_contract()
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
  name: "analytical_crs04_stage31_v0_5",
  description: "Stage 03 section 3.1 SPSS-authority shadow model.",
  tags: ["stage03", "analytical", "stage31", "shadow"]
}}

WITH
{",\n\n".join(ctes)}

SELECT
{final_select}
FROM {previous}
'''


def render_quality_assertion() -> str:
    return '''config {
  type: "assertion",
  schema: "enares2024_crs04_ops",
  tags: ["stage03", "analytical", "stage31", "quality"]
}

WITH
candidate AS (
  SELECT *
  FROM ${ref("analytical_crs04_stage31_v0_5")}
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
)

SELECT *
FROM checks
'''


def render_parity_assertion() -> str:
    _, blocks = build_stage31_contract()
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
  tags: ["stage03", "analytical", "stage31", "parity"]
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
  FROM ${{ref("analytical_crs04_stage31_v0_5")}}
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
    _, blocks = build_stage31_contract()
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
