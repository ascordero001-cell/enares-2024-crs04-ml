from pathlib import Path

import yaml

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
    assert "ruff==0.16.8" in requirements


def test_mypy_checks_stage04_across_module_boundaries() -> None:
    config = (ROOT / "mypy.ini").read_text(encoding="utf-8")
    assert "follow_imports = normal" in config
    assert "[mypy-scripts.*]" in config
    assert "Legacy Stage 03 generator scripts" in config


def test_security_ci_audits_dependencies_and_complete_git_history() -> None:
    workflow_path = ROOT / ".github" / "workflows" / "security-ci.yml"
    workflow = workflow_path.read_text(encoding="utf-8")
    parsed = yaml.safe_load(workflow)

    assert parsed["permissions"] == {"contents": "read"}
    for required in (
        "pypa/gh-action-pip-audit@v1.1.0",
        "inputs: requirements.txt requirements-dev.txt",
        "gitleaks/gitleaks-action@v3",
        "fetch-depth: 0",
        'GITLEAKS_ENABLE_COMMENTS: "false"',
        "Prove a synthetic canary blocks the scanner",
        "ghcr.io/gitleaks/gitleaks:v8.24.3",
        "--exit-code 23",
        '--redact',
    ):
        assert required in workflow


def test_dependabot_monitors_python_and_github_actions_weekly() -> None:
    config = yaml.safe_load(
        (ROOT / ".github" / "dependabot.yml").read_text(encoding="utf-8")
    )
    updates = config["updates"]

    assert {entry["package-ecosystem"] for entry in updates} == {
        "pip",
        "github-actions",
    }
    assert all(entry["directory"] == "/" for entry in updates)
    assert all(entry["schedule"]["interval"] == "weekly" for entry in updates)


def test_gitleaks_configuration_extends_defaults_with_safe_canary() -> None:
    config = (ROOT / ".gitleaks.toml").read_text(encoding="utf-8")

    assert "useDefault = true" in config
    assert 'id = "stage04-synthetic-canary"' in config
    assert "STAGE04_CANARY_[A-Z0-9]{32}" in config
