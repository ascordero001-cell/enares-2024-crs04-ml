from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_app_ci_runs_quality_gates_and_builds_without_publishing() -> None:
    workflow = (ROOT / ".github" / "workflows" / "app-ci.yml").read_text(
        encoding="utf-8"
    )

    for required in (
        "app-quality:",
        "docker-build:",
        "ruff check src app tests",
        "mypy --config-file mypy.ini src app tests",
        "python -m pytest -q",
        "docker build --tag enares-stage04:app-ci .",
    ):
        assert required in workflow
    assert "docker push" not in workflow
    assert "gcloud" not in workflow


def test_quality_tools_are_pinned() -> None:
    requirements = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
    assert "mypy==1.18.2" in requirements
    assert "ruff==0.16.7" in requirements


def test_mypy_checks_stage04_across_module_boundaries() -> None:
    config = (ROOT / "mypy.ini").read_text(encoding="utf-8")
    assert "follow_imports = normal" in config
    assert "[mypy-scripts.*]" in config
    assert "Legacy Stage 03 generator scripts" in config
