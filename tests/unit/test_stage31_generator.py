from scripts.generate_stage31_dataform import (
    build_stage31_contract,
    output_columns,
    render_model,
    render_parity_assertion,
    render_quality_assertion,
)


def test_stage31_contract_has_expected_block_and_column_counts():
    raw_inputs, blocks = build_stage31_contract()

    assert len(blocks) == 10
    assert [len(expressions) for _, expressions in blocks] == [
        13,
        1,
        6,
        4,
        1,
        30,
        7,
        3,
        4,
        2,
    ]
    assert len(output_columns(blocks)) == 71
    assert len(set(output_columns(blocks))) == 71
    assert {"CCDD", "CCPP", "SEXO", "C3P301_4"}.issubset(raw_inputs)


def test_stage31_contract_preserves_validated_pilot_formula():
    _, blocks = build_stage31_contract()
    expressions = {
        column: expression
        for _, block in blocks
        for column, expression in block.items()
    }

    assert expressions["justifica_castigo_docente"] == (
        "CASE WHEN C3P301_4 = 1 THEN 1 WHEN C3P301_4 = 2 THEN 0 END"
    )
    assert "SAFE_DIVIDE" in expressions["prop_tareas_femeninas"]
    assert "LPAD(CAST(CCDD AS STRING)" in expressions["DEPARTAMENTO2"]


def test_stage31_model_renders_ordered_ctes_and_all_aliases():
    _, blocks = build_stage31_contract()
    model = render_model()

    assert '${ref("cleaned_crs04_merged_adolescents_v0_5")}' in model
    assert "block_01_31_factores" in model
    assert "block_10_31_mitos_agregados" in model
    for column in output_columns(blocks):
        assert f"AS `{column}`" in model or f"`{column}`\n" in model


def test_stage31_assertions_cover_integrity_and_every_output():
    _, blocks = build_stage31_contract()
    quality = render_quality_assertion()
    parity = render_parity_assertion()

    assert "duplicate_key_groups" in quality
    assert "survey_design_fields" in quality
    assert '${ref("analytical_crs04_adolescents")}' in parity
    for column in output_columns(blocks):
        assert (
            f"candidate.`{column}` IS DISTINCT FROM reference.`{column}`"
            in parity
        )
