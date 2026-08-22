import pytest

from enares.config import load_config


ENVIRONMENT_KEYS = (
    "PROJECT_ID",
    "BQ_LOCATION",
    "BQ_RAW_DATASET",
    "BQ_CLEANED_DATASET",
    "BQ_ANALYTICAL_DATASET",
    "BQ_OUTPUTS_DATASET",
    "BQ_PUBLISHED_DATASET",
    "BQ_OPS_DATASET",
)


def clear_environment(monkeypatch):
    for key in ENVIRONMENT_KEYS:
        monkeypatch.delenv(key, raising=False)


def test_load_config_uses_safe_defaults(monkeypatch):
    clear_environment(monkeypatch)

    config = load_config()

    assert config.project_id == "enares-2024-crs04"
    assert config.location == "US"
    assert config.datasets.raw == "enares2024_crs04_raw"
    assert config.datasets.cleaned == "enares2024_crs04_cleaned"
    assert config.datasets.analytical == "enares2024_crs04_analytical"


def test_load_config_accepts_environment_overrides(monkeypatch):
    clear_environment(monkeypatch)
    monkeypatch.setenv("PROJECT_ID", "test-project")
    monkeypatch.setenv("BQ_RAW_DATASET", "test_raw")

    config = load_config()

    assert config.project_id == "test-project"
    assert config.datasets.raw == "test_raw"


def test_load_config_rejects_empty_values(monkeypatch):
    clear_environment(monkeypatch)
    monkeypatch.setenv("PROJECT_ID", "   ")

    with pytest.raises(ValueError, match="PROJECT_ID cannot be empty"):
        load_config()