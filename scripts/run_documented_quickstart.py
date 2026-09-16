"""Execute one explicitly labelled command block from a Markdown quickstart."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

FENCE_PATTERN = re.compile(
    r"^```(?P<info>[^\n]*)\n(?P<body>.*?)^```\s*$",
    flags=re.MULTILINE | re.DOTALL,
)
FORBIDDEN_COMMANDS = ("gcloud", "bq ")


def extract_command_block(markdown: str, marker: str) -> str:
    """Return the single fenced block whose info string contains ``marker``."""
    matches = [
        match.group("body").strip()
        for match in FENCE_PATTERN.finditer(markdown)
        if marker in match.group("info").split()
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one Markdown block marked {marker!r}; found {len(matches)}"
        )

    commands = matches[0]
    lowered = commands.casefold()
    forbidden = [token for token in FORBIDDEN_COMMANDS if token in lowered]
    if forbidden:
        raise ValueError(f"Quickstart block contains forbidden cloud commands: {forbidden}")
    return commands


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("--block", default="quickstart-ci")
    args = parser.parse_args()

    commands = extract_command_block(args.document.read_text(encoding="utf-8"), args.block)
    subprocess.run(["bash", "-euxo", "pipefail", "-c", commands], check=True)


if __name__ == "__main__":
    main()
