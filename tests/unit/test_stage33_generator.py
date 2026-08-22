from scripts.generate_stage33_dataform import (
    build_stage33_contract,
    output_columns,
    render_model,
    render_parity_assertion,
    render_quality_assertion,
)


def stage33_expressions() -> dict[str, str]:
    _, blocks = build_stage33_contract()
    return {
        column: expression
        for _, block in blocks
        for column, expression in block.items()
    }


def test_stage33_contract_has_expected_block_and_column_counts():
    raw_inputs, blocks = build_stage33_contract()

    assert len(blocks) == 3
    assert [len(expressions) for _, expressions in blocks] == [24, 9, 18]
    assert len(output_columns(blocks)) == 51
    assert len(set(output_columns(blocks))) == 51
    assert {
        "C3P225",
        "C3P229",
        "C3P223_14",
        "C3P223B_14",
        "C3P227D_10",
    }.issubset(raw_inputs)


def test_stage33_contract_preserves_validated_school_pilot_formula():
    expressions = stage33_expressions()

    assert expressions["C3P223_1_1"] == (
        "CASE WHEN C3P223_1 = 1 AND C3P225 = 1 "
        "AND (C3P223A_1 = 1 OR C3P223C_1 = 1 "
        "OR C3P223E_1 = 1) THEN 1 ELSE 0 END"
    )
    assert expressions["VP_ESCUELA"] == (
        "CASE WHEN (`C3P223_1_1` = 1 OR `C3P223_2_1` = 1 "
        "OR `C3P223_3_1` = 1 OR `C3P223_4_1` = 1 "
        "OR `C3P223_5_1` = 1 OR `C3P223_6_1` = 1 "
        "OR `C3P223_7_1` = 1 OR `C3P223_8_1` = 1 "
        "OR `C3P223_9_1` = 1 OR `C3P223_10_1` = 1 "
        "OR `C3P223_11_1` = 1 OR `C3P223_12_1` = 1 "
        "OR `C3P223_13_1` = 1 OR `C3P223_14_1` = 1) "
        "THEN 1 ELSE 0 END"
    )


def test_stage33_contract_contains_all_published_aggressor_groups():
    expressions = stage33_expressions()

    for prefix in ("AG_VP_E", "AG_VF_E"):
        for index in range(1, 10):
            assert f"{prefix}_{index:02d}" in expressions
    assert "C3P223B_1 = 1" in expressions["AG_VP_E_02"]
    assert "C3P227D_10 = 3" in expressions["AG_VF_E_08"]
    assert "C3P223E_14 = 1" in expressions["AG_VP_E_09"]


def test_stage33_model_renders_ordered_ctes_and_all_aliases():
    _, blocks = build_stage33_contract()
    model = render_model()

    assert '${ref("cleaned_crs04_merged_adolescents_v0_5")}' in model
    assert "block_01_33_escuela_formas" in model
    assert "block_03_331_escuela_agresores" in model
    assert model.index("block_01_33_escuela_formas") < model.index(
        "block_03_331_escuela_agresores"
    )
    for column in output_columns(blocks):
        assert f"AS `{column}`" in model or f"`{column}`\n" in model


def test_stage33_assertions_cover_integrity_binary_values_and_every_output():
    _, blocks = build_stage33_contract()
    quality = render_quality_assertion()
    parity = render_parity_assertion()

    assert "duplicate_key_groups" in quality
    assert "survey_design_fields" in quality
    assert "binary_outputs" in quality
    assert '${ref("analytical_crs04_adolescents")}' in parity
    for column in output_columns(blocks):
        assert f"`{column}` NOT IN (0, 1)" in quality
        assert (
            f"candidate.`{column}` IS DISTINCT FROM reference.`{column}`"
            in parity
        )
