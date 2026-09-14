"""Build the Stage 04 Etapa 1 authorized aggregate from its private V0 parent."""

from __future__ import annotations

import argparse
from pathlib import Path

from enares.stage04.authorized_extract import build_etapa1_authorized_extract


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("parent", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--parent-sha256", required=True)
    parser.add_argument("--git-commit-sha", required=True)
    parser.add_argument("--generated-at-utc")
    args = parser.parse_args()
    build_etapa1_authorized_extract(
        args.parent,
        args.output,
        args.manifest,
        expected_parent_sha256=args.parent_sha256,
        git_commit_sha=args.git_commit_sha,
        generated_at_utc=args.generated_at_utc,
    )


if __name__ == "__main__":
    main()
