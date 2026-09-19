"""Fail-closed preparation for a manually authorized Stage 04 aggregate."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from .repository import AuthorizedAggregateRepository, IndicatorEstimate
from .validation import validate_estimates

MODULE_IDS = ("3.1", "3.2", "3.3", "3.4", "3.5", "3.6")
RESERVED_IDENTITIES = frozenset({"UNPROMOTED", "__UNPROMOTED__"})
IDENTITY_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{2,127}")
SHA256_PATTERN = re.compile(r"[0-9a-fA-F]{64}")
COMMIT_PATTERN = re.compile(r"[0-9a-fA-F]{40}")


@dataclass(frozen=True)
class PipelineInputContract:
    """Immutable human-approved identity for one private-input run."""

    release_id: str
    run_id: str
    aggregate_sha256: str
    manifest_sha256: str
    parent_sha256: str
    expected_row_count: int
    expected_indicator_count: int
    decision_reference: str
    decision_commit: str

    def validate(self) -> None:
        for name, value in (
            ("release_id", self.release_id),
            ("run_id", self.run_id),
        ):
            if not IDENTITY_PATTERN.fullmatch(value) or value in RESERVED_IDENTITIES:
                raise ValueError(f"{name} is invalid or reserved")
        for name, value in (
            ("aggregate_sha256", self.aggregate_sha256),
            ("manifest_sha256", self.manifest_sha256),
            ("parent_sha256", self.parent_sha256),
        ):
            if not SHA256_PATTERN.fullmatch(value):
                raise ValueError(f"{name} must be a SHA-256")
        if not COMMIT_PATTERN.fullmatch(self.decision_commit):
            raise ValueError("decision_commit must be a full commit SHA")
        if not self.decision_reference.startswith("https://github.com/"):
            raise ValueError("decision_reference must be a GitHub evidence URL")
        if self.expected_row_count <= 0 or self.expected_indicator_count <= 0:
            raise ValueError("expected counts must be positive")


@dataclass(frozen=True)
class PreparedAggregateEvidence:
    """Safe evidence fields; private paths and row contents are intentionally absent."""

    status: str
    release_id: str
    run_id: str
    aggregate_sha256: str
    manifest_sha256: str
    parent_sha256: str
    row_count: int
    indicator_count: int
    module_row_counts: dict[str, int]
    decision_reference: str
    decision_commit: str
    synthetic_rows: int
    non_approved_rows: int

    def as_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    def as_markdown(self) -> str:
        modules = "\n".join(
            f"- {module_id}: {count} filas"
            for module_id, count in self.module_row_counts.items()
        )
        return (
            "# Evidencia previa de agregado Stage 04\n\n"
            f"- Estado: `{self.status}`\n"
            f"- Release/run: `{self.release_id}` / `{self.run_id}`\n"
            f"- SHA-256 del agregado: `{self.aggregate_sha256}`\n"
            f"- SHA-256 del manifiesto: `{self.manifest_sha256}`\n"
            f"- SHA-256 del padre V0: `{self.parent_sha256}`\n"
            f"- Filas/indicadores: {self.row_count} / {self.indicator_count}\n"
            f"- Filas sintéticas: {self.synthetic_rows}\n"
            f"- Filas no aprobadas: {self.non_approved_rows}\n"
            f"- Decisión: {self.decision_reference}\n"
            f"- Commit de decisión: `{self.decision_commit}`\n\n"
            "## Cobertura\n\n"
            f"{modules}\n\n"
            "La evidencia no contiene filas, rutas privadas, principales, credenciales ni "
            "identificadores de jobs. Este resultado no autoriza carga, promoción ni publicación.\n"
        )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_authorized_aggregate(
    contract: PipelineInputContract,
    *,
    aggregate_path: Path,
    manifest_path: Path,
    approval_registry_path: Path,
) -> PreparedAggregateEvidence:
    """Verify provenance and runtime contracts without mutating cloud state."""
    contract.validate()
    if not aggregate_path.is_file() or not manifest_path.is_file():
        raise ValueError("The manually authorized per-run input is unavailable")
    if _sha256(aggregate_path).lower() != contract.aggregate_sha256.lower():
        raise ValueError("Aggregate SHA-256 does not match the approved run contract")
    if _sha256(manifest_path).lower() != contract.manifest_sha256.lower():
        raise ValueError("Manifest SHA-256 does not match the approved run contract")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Manifest is unavailable or invalid") from exc
    if manifest.get("sha256", "").lower() != contract.aggregate_sha256.lower():
        raise ValueError("Manifest is not bound to the approved aggregate")
    if manifest.get("source_hash", "").lower() != contract.parent_sha256.lower():
        raise ValueError("Manifest parent does not match the approved V0 parent")
    if manifest.get("parent_sha256", "").lower() != contract.parent_sha256.lower():
        raise ValueError("Manifest parent_sha256 is inconsistent")
    if manifest.get("row_count") != contract.expected_row_count:
        raise ValueError("Manifest row count does not match the approved run contract")
    if manifest.get("indicator_count") != contract.expected_indicator_count:
        raise ValueError("Manifest indicator count does not match the approved run contract")

    repository = AuthorizedAggregateRepository(
        aggregate_path,
        manifest_path,
        approval_registry_path,
    )
    rows: list[IndicatorEstimate] = []
    module_row_counts: dict[str, int] = {}
    for module_id in MODULE_IDS:
        module_rows = repository.list_estimates(module_id)
        module_row_counts[module_id] = len(module_rows)
        rows.extend(module_rows)
    validate_estimates(rows)

    if len(rows) != contract.expected_row_count:
        raise ValueError("Verified row count does not match the approved run contract")
    if len({row.indicator_id for row in rows}) != contract.expected_indicator_count:
        raise ValueError("Verified indicator count does not match the approved run contract")
    if {row.release_id for row in rows} != {contract.release_id}:
        raise ValueError("Aggregate release_id does not match the approved run contract")
    if {row.run_id for row in rows} != {contract.run_id}:
        raise ValueError("Aggregate run_id does not match the approved run contract")
    if any(row.source_hash.lower() != contract.parent_sha256.lower() for row in rows):
        raise ValueError("Aggregate rows do not match the approved V0 parent")

    evidence = PreparedAggregateEvidence(
        status="PASS_PREPARED_NO_CLOUD_MUTATION",
        release_id=contract.release_id,
        run_id=contract.run_id,
        aggregate_sha256=contract.aggregate_sha256.lower(),
        manifest_sha256=contract.manifest_sha256.lower(),
        parent_sha256=contract.parent_sha256.lower(),
        row_count=len(rows),
        indicator_count=len({row.indicator_id for row in rows}),
        module_row_counts=module_row_counts,
        decision_reference=contract.decision_reference,
        decision_commit=contract.decision_commit.lower(),
        synthetic_rows=sum(row.synthetic for row in rows),
        non_approved_rows=sum(row.validation_status != "APPROVED" for row in rows),
    )
    if evidence.synthetic_rows or evidence.non_approved_rows:
        raise ValueError("Only approved, provenance-derived institutional rows are accepted")
    return evidence
