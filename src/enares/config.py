"""Environment-independent configuration for the ENARES pipeline."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class DatasetConfig:
    raw: str
    cleaned: str
    analytical: str
    outputs: str
    published: str
    ops: str


@dataclass(frozen=True)
class ProjectConfig:
    project_id: str
    location: str
    datasets: DatasetConfig


def _setting(name: str, default: str) -> str:
    value = os.getenv(name, default).strip()
    if not value:
        raise ValueError(f"{name} cannot be empty")
    return value


def load_config() -> ProjectConfig:
    """Load non-secret project settings from environment variables."""

    return ProjectConfig(
        project_id=_setting("PROJECT_ID", "enares-2024-crs04"),
        location=_setting("BQ_LOCATION", "US"),
        datasets=DatasetConfig(
            raw=_setting("BQ_RAW_DATASET", "enares2024_crs04_raw"),
            cleaned=_setting(
                "BQ_CLEANED_DATASET",
                "enares2024_crs04_cleaned",
            ),
            analytical=_setting(
                "BQ_ANALYTICAL_DATASET",
                "enares2024_crs04_analytical",
            ),
            outputs=_setting(
                "BQ_OUTPUTS_DATASET",
                "enares2024_crs04_outputs",
            ),
            published=_setting(
                "BQ_PUBLISHED_DATASET",
                "enares2024_crs04_published",
            ),
            ops=_setting("BQ_OPS_DATASET", "enares2024_crs04_ops"),
        ),
    )