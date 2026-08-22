from scripts.generate_stage32_dataform import (
    build_stage32_contract,
    output_columns,
    render_model,
    render_parity_assertion,
    render_quality_assertion,
)


def stage32_expressions() -> dict[str, str]:
    _, blocks = build_stage32_contract()
    return {
        column: expression
        for _, block in blocks
        for column, expression in block.items()
    }


def test_stage32_contract_has_expected_block_and_column_counts():
    raw_inputs, blocks = build_stage32_contract()

    assert len(blocks) == 6
    assert [len(expressions) for _, expressions in blocks] == [
        18,
        4,
        4,
        1,
        7,
        16,
    ]
    assert len(output_columns(blocks)) == 50
    assert len(set(output_columns(blocks))) == 50
    assert {
        "SEXO",
        "C3P203",
        "C3P207",
        "C3P201_11",
        "C3P205F_7",
    }.issubset(raw_inputs)


def test_stage32_contract_preserves_validated_household_pilot_formula():
    expressions = stage32_expressions()

    assert "C3P201_1 = 1" in expressions["C3P201_1_1"]
    assert "C3P203 = 1" in expressions["C3P201_1_1"]
    assert expressions["VP_HOGAR"] == (
        "CASE WHEN (`C3P201_1_1` = 1 OR `C3P201_2_1` = 1 "
        "OR `C3P201_3_1` = 1 OR `C3P201_4_1` = 1 "
        "OR `C3P201_5_1` = 1 OR `C3P201_6_1` = 1 "
        "OR `C3P201_7_1` = 1 OR `C3P201_8_1` = 1 "
        "OR `C3P201_9_1` = 1 OR `C3P201_10_1` = 1 "
        "OR `C3P201_11_1` = 1) THEN 1 ELSE 0 END"
    )


def test_stage32_contract_contains_all_published_groups():
    expressions = stage32_expressions()

    for prefix in ("AG_VP_H", "AG_VF_H"):
        for index in range(1, 9):
            assert f"{prefix}_{index:02d}" in expressions
    assert expressions["Solap_VP_VF_H__Coexistencia"] == "VP_VF_HOGAR"
    assert "C3P216A_6C = 1" in expressions["VF_HOGAR_03"]
    assert "C3P216C_5C = 1" in expressions["VF_HOGAR_03"]


def test_stage32_model_renders_ordered_ctes_and_all_aliases():
    _, blocks = build_stage32_contract()
    model = render_model()

    assert '${ref("cleaned_crs04_merged_adolescents_v0_5")}' in model
    assert "block_01_32_hogar_formas" in model
    assert "block_06_321_hogar_agresores" in model
    assert model.index("block_01_32_hogar_formas") < model.index(
        "block_06_321_hogar_agresores"
    )
    for column in output_columns(blocks):
        assert f"AS `{column}`" in model or f"`{column}`\n" in model


def test_stage32_assertions_cover_integrity_binary_values_and_every_output():
    _, blocks = build_stage32_contract()
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
