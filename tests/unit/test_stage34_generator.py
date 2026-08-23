from scripts.generate_stage34_dataform import (
    HOUSEHOLD_DEPENDENCIES,
    SCHOOL_DEPENDENCIES,
    build_stage34_contract,
    output_columns,
    render_model,
    render_parity_assertion,
    render_quality_assertion,
)


def stage34_expressions() -> dict[str, str]:
    _, blocks = build_stage34_contract()
    return {
        column: expression
        for _, block in blocks
        for column, expression in block.items()
    }


def test_stage34_contract_has_authority_block_and_column_counts():
    raw_inputs, blocks = build_stage34_contract()

    assert len(blocks) == 7
    assert [len(expressions) for _, expressions in blocks] == [
        80,
        6,
        78,
        2,
        18,
        3,
        237,
    ]
    assert len(output_columns(blocks)) == 424
    assert len(set(output_columns(blocks))) == 424
    assert {
        "SEXO",
        "C4P248_16",
        "C4P248A_28_16",
        "C4P248B_16",
        "C4P248C_16",
        "C4P248_O_12",
    }.issubset(raw_inputs)


def test_stage34_contract_preserves_core_spss_formulas():
    expressions = stage34_expressions()

    assert expressions["P248_01_12M"] == (
        "CASE WHEN C4P248_1 = 1 AND C4P248C_1 = 1 THEN 1 ELSE 0 END"
    )
    assert "C4P248A_27_1 = 1" in expressions["C4P248_1_1"]
    assert "C4P248A_17_1 = 1" in expressions["C4P248_1_3"]
    assert "ACOSO SEXUAL" in expressions["INDICADOR_8_2_13"]
    assert expressions["VS_ICVAC_CONTACTO"] == (
        "CASE WHEN VS_ICVAC_301 = 1 OR VS_ICVAC_302 = 1 "
        "THEN 1 ELSE 0 END"
    )


def test_stage34_contract_contains_all_aggressors_and_published_aliases():
    expressions = stage34_expressions()

    for prefix in ("AG_VS12", "AG_VSVIDA"):
        for index in range(1, 10):
            assert f"{prefix}_{index:02d}" in expressions
    assert expressions["AG_VP_09"] == "AG_VP_E_09"
    assert expressions["Agresor_VP_H__AG_VP_08"] == "AG_VP_H_08"
    assert expressions["Prev_Agresor_VS__AG_08"] == "AG_VS12_08"
    assert expressions["Prev_Agresor_VS__AG_07"] == "AG_VSVIDA_07"
    assert len(HOUSEHOLD_DEPENDENCIES) == 16
    assert len(SCHOOL_DEPENDENCIES) == 18


def test_stage34_model_joins_prior_shadow_batches_and_renders_ordered_ctes():
    _, blocks = build_stage34_contract()
    model = render_model()

    assert '${ref("cleaned_crs04_merged_adolescents_v0_5")}' in model
    assert '${ref("analytical_crs04_stage32_v0_5")}' in model
    assert '${ref("analytical_crs04_stage33_v0_5")}' in model
    assert "block_01_34_vs_formas_contexto" in model
    assert "block_07_34_aliases_spss" in model
    assert model.index("block_01_34_vs_formas_contexto") < model.index(
        "block_07_34_aliases_spss"
    )
    for column in output_columns(blocks):
        assert f"AS `{column}`" in model or f"`{column}`\n" in model


def test_stage34_assertions_cover_integrity_binary_values_and_every_output():
    _, blocks = build_stage34_contract()
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
