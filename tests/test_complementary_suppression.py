import pytest

from enares.stage04.privacy import (
    PUBLICATION_CHANNELS,
    apply_published_suppression,
    assert_consistent_suppression_within_release,
    assert_no_reconstructable_primary,
    assert_no_retroactive_suppression,
    assert_no_unique_additive_reconstruction,
    assert_suppressed_fields_are_null,
    derive_primary_confidentiality,
    materialize_safe_channel_payloads,
    plan_complementary_suppression,
)


def synthetic_partition():
    return [
        {
            "cell_id": "total",
            "parent_total_id": None,
            "estimate": 100.0,
            "standard_error": 0.0,
            "ci95_lower": 100.0,
            "ci95_upper": 100.0,
            "cv": 0.0,
            "n_unweighted": 100,
            "weighted_population": 1000.0,
            "suppress_flag": False,
        },
        {
            "cell_id": "group_a",
            "parent_total_id": "total",
            "estimate": 7.0,
            "standard_error": 1.0,
            "ci95_lower": 5.0,
            "ci95_upper": 9.0,
            "cv": 0.14,
            "n_unweighted": 7,
            "weighted_population": 70.0,
            "suppress_flag": True,
        },
        {
            "cell_id": "group_b",
            "parent_total_id": "total",
            "estimate": 93.0,
            "standard_error": 1.0,
            "ci95_lower": 91.0,
            "ci95_upper": 95.0,
            "cv": 0.01,
            "n_unweighted": 93,
            "weighted_population": 930.0,
            "suppress_flag": False,
        },
    ]


def test_primary_suppression_alone_is_reconstructible():
    with pytest.raises(ValueError, match="uniquely reconstructed"):
        assert_no_unique_additive_reconstruction(synthetic_partition())


def test_complementary_suppression_prevents_unique_reconstruction():
    rows = synthetic_partition()
    rows[2]["suppress_flag"] = True
    assert_no_unique_additive_reconstruction(rows)


def test_suppression_is_materialized_in_published_layer():
    rows = synthetic_partition()
    rows[2]["suppress_flag"] = True
    published = apply_published_suppression(rows)
    assert_suppressed_fields_are_null(published)
    for row in published[1:]:
        assert row["estimate"] is None
        assert row["ci95_lower"] is None
        assert row["ci95_upper"] is None
        assert row["n_unweighted"] is None
        assert row["weighted_population"] is None


def test_suppressed_weighted_population_is_rejected_before_materialization():
    rows = synthetic_partition()
    with pytest.raises(ValueError, match="exposes"):
        assert_suppressed_fields_are_null(rows)


def test_non_suppressed_weighted_population_is_preserved():
    published = apply_published_suppression(synthetic_partition())
    assert published[0]["weighted_population"] == 1000.0


def test_visual_only_suppression_fails_published_contract():
    rows = synthetic_partition()
    with pytest.raises(ValueError, match="exposes"):
        assert_suppressed_fields_are_null(rows)


@pytest.mark.parametrize(
    ("target", "base", "dominance", "expected"),
    (
        (2, 100, False, ("SENSITIVE_EVENT_COUNT_1_TO_4",)),
        (97, 100, False, ("SENSITIVE_COMPLEMENT_COUNT_1_TO_4",)),
        (20, 25, False, ()),
        (0, 20, False, ()),
        (20, 100, True, ("PRODUCER_DOMINANCE_FLAG",)),
    ),
)
def test_primary_rule_is_independent_of_precision_thresholds(
    target, base, dominance, expected
):
    assert (
        derive_primary_confidentiality(
            target_unweighted=target,
            base_unweighted=base,
            producer_dominance_flag=dominance,
        )
        == expected
    )


@pytest.mark.parametrize(
    "kwargs",
    (
        {"target_unweighted": -1, "base_unweighted": 10},
        {"target_unweighted": 11, "base_unweighted": 10},
    ),
)
def test_primary_rule_fails_closed_on_invalid_counts(kwargs):
    with pytest.raises(ValueError, match="valid base"):
        derive_primary_confidentiality(**kwargs)


def protected_cell(
    cell_id,
    *,
    release_id="release-2",
    table_id="table-a",
    suppression_type=None,
    suppress_flag=False,
    base_unw=100,
    eligible_for_complementary=False,
):
    return {
        "cell_id": cell_id,
        "release_id": release_id,
        "table_id": table_id,
        "suppression_type": suppression_type,
        "suppress_flag": suppress_flag,
        "estimate": 10.0,
        "standard_error": 1.0,
        "ci95_lower": 8.0,
        "ci95_upper": 12.0,
        "cv": 0.1,
        "n_unweighted": 100,
        "weighted_population": 1000.0,
        "base_unw": base_unw,
        "eligible_for_complementary": eligible_for_complementary,
    }


def test_same_release_cannot_show_a_cell_in_one_table_and_hide_it_in_another():
    rows = [
        protected_cell("shared", table_id="table-a", suppress_flag=True),
        protected_cell("shared", table_id="table-b", suppress_flag=False),
    ]
    with pytest.raises(ValueError, match="inconsistent suppression"):
        assert_consistent_suppression_within_release(rows)


def test_combined_equations_detect_reconstruction_not_visible_table_by_table():
    rows = [
        protected_cell("primary", suppression_type="PRIMARY", suppress_flag=True),
        protected_cell(
            "a",
            table_id="table-a",
            suppression_type="COMPLEMENTARY",
            suppress_flag=True,
        ),
        protected_cell(
            "b",
            table_id="table-b",
            suppression_type="COMPLEMENTARY",
            suppress_flag=True,
        ),
        protected_cell("total-a", table_id="table-a"),
        protected_cell("total-b", table_id="table-b"),
        protected_cell("total-c", table_id="table-c"),
    ]
    equations = [
        {"equation_id": "table-a", "terms": {"primary": 1, "a": 1, "total-a": -1}},
        {"equation_id": "table-b", "terms": {"primary": 1, "b": 1, "total-b": -1}},
        {"equation_id": "table-c", "terms": {"a": 1, "b": 1, "total-c": -1}},
    ]
    with pytest.raises(ValueError, match="combined equation system"):
        assert_no_reconstructable_primary(rows, equations)

    rows.append(
        protected_cell(
            "c",
            table_id="table-c",
            suppression_type="COMPLEMENTARY",
            suppress_flag=True,
        )
    )
    equations[2]["terms"]["c"] = 1
    assert_no_reconstructable_primary(rows, equations)


def test_complementary_plan_uses_lowest_base_then_cell_id_deterministically():
    rows = [
        protected_cell("primary", suppression_type="PRIMARY", suppress_flag=True),
        protected_cell("z", base_unw=20, eligible_for_complementary=True),
        protected_cell("b", base_unw=10, eligible_for_complementary=True),
        protected_cell("a", base_unw=10, eligible_for_complementary=True),
    ]
    equations = [
        {
            "equation_id": "margin",
            "terms": {"primary": 1, "z": 1, "b": 1, "a": 1},
        }
    ]
    planned = plan_complementary_suppression(rows, equations)
    decisions = {row["cell_id"]: row for row in planned}
    assert decisions["a"]["suppression_type"] == "COMPLEMENTARY"
    assert decisions["a"]["suppression_reason"] == (
        "PROTECT_PRIMARY_FROM_RECONSTRUCTION"
    )
    assert decisions["b"]["suppress_flag"] is False
    assert decisions["z"]["suppress_flag"] is False


def test_complementary_plan_fails_closed_when_no_candidate_is_available():
    rows = [
        protected_cell("primary", suppression_type="PRIMARY", suppress_flag=True),
        protected_cell("visible"),
    ]
    equations = [{"equation_id": "margin", "terms": {"primary": 1, "visible": 1}}]
    with pytest.raises(ValueError, match="No safe complementary"):
        plan_complementary_suppression(rows, equations)


def test_cross_release_equations_are_evaluated_as_one_system():
    rows = [
        protected_cell("primary", suppression_type="PRIMARY", suppress_flag=True),
        protected_cell("a", suppression_type="COMPLEMENTARY", suppress_flag=True),
        protected_cell(
            "b",
            release_id="release-1",
            suppression_type="COMPLEMENTARY",
            suppress_flag=True,
        ),
    ]
    equations = [
        {"equation_id": "release-2-a", "terms": {"primary": 1, "a": 1}},
        {"equation_id": "release-1-b", "terms": {"primary": 1, "b": 1}},
        {"equation_id": "cross-release", "terms": {"a": 1, "b": 1}},
    ]
    with pytest.raises(ValueError, match="combined equation system"):
        assert_no_reconstructable_primary(rows, equations)


def test_visible_history_cannot_be_made_private_retroactively():
    history = [protected_cell("shared", release_id="release-1")]
    candidate = [
        protected_cell(
            "shared",
            suppression_type="PRIMARY",
            suppress_flag=True,
        )
    ]
    with pytest.raises(ValueError, match="previously visible"):
        assert_no_retroactive_suppression(candidate, history)


def test_every_outward_channel_receives_only_nullified_protected_fields():
    rows = [
        protected_cell(
            "primary",
            suppression_type="PRIMARY",
            suppress_flag=True,
        )
    ]
    payloads = materialize_safe_channel_payloads(rows)
    assert set(payloads) == set(PUBLICATION_CHANNELS)
    for payload in payloads.values():
        assert all(
            payload[0][field] is None
            for field in (
                "estimate",
                "standard_error",
                "ci95_lower",
                "ci95_upper",
                "cv",
                "n_unweighted",
                "weighted_population",
            )
        )
        assert payload[0]["suppression_type"] == "PRIMARY"
