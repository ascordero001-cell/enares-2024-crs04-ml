import pytest

from enares.stage04.privacy import (
    apply_published_suppression,
    assert_no_unique_additive_reconstruction,
    assert_suppressed_fields_are_null,
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


def test_visual_only_suppression_fails_published_contract():
    rows = synthetic_partition()
    with pytest.raises(ValueError, match="exposes"):
        assert_suppressed_fields_are_null(rows)
