from pathlib import Path

import pytest

from scripts.run_documented_quickstart import extract_command_block

QUICKSTART = Path("docs/stage04/demo_local_quickstart.md")


def test_stage04_quickstart_has_one_executable_ci_block() -> None:
    commands = extract_command_block(QUICKSTART.read_text(encoding="utf-8"), "quickstart-ci")

    assert "python -m pytest -q" in commands
    assert "scripts/release_diagnostic.py" in commands
    assert "/_stcore/health" in commands


def test_quickstart_block_must_be_unique() -> None:
    markdown = "```bash quickstart-ci\necho one\n```\n```bash quickstart-ci\necho two\n```\n"

    with pytest.raises(ValueError, match="found 2"):
        extract_command_block(markdown, "quickstart-ci")


@pytest.mark.parametrize("command", ["gcloud projects list", "bq query 'SELECT 1'"])
def test_quickstart_block_rejects_cloud_commands(command: str) -> None:
    markdown = f"```bash quickstart-ci\n{command}\n```\n"

    with pytest.raises(ValueError, match="forbidden cloud commands"):
        extract_command_block(markdown, "quickstart-ci")
