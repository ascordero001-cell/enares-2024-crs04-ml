"""Release-scoped cache for validated aggregate repository results."""

from __future__ import annotations

from collections.abc import Iterable

from enares.stage04.release_lifecycle import ReleaseKey
from enares.stage04.repository import (
    RELEASE_NOT_FOUND_MESSAGE,
    IndicatorEstimate,
    ReleaseNotFoundError,
    RepositoryContractError,
)


class ReleaseRunCache:
    """Keep immutable snapshots isolated by both release and run identifiers."""

    def __init__(self) -> None:
        self._entries: dict[ReleaseKey, tuple[IndicatorEstimate, ...]] = {}

    def store(self, rows: Iterable[IndicatorEstimate]) -> ReleaseKey:
        snapshot = tuple(rows)
        keys = {ReleaseKey(row.release_id, row.run_id) for row in snapshot}
        if len(keys) != 1:
            raise RepositoryContractError(
                "A cache snapshot must contain exactly one release run"
            )
        key = keys.pop()
        if key in self._entries:
            raise RepositoryContractError("A cached release run cannot be overwritten")
        self._entries[key] = snapshot
        return key

    def get(self, key: ReleaseKey) -> tuple[IndicatorEstimate, ...]:
        try:
            return self._entries[key]
        except KeyError:
            raise ReleaseNotFoundError(RELEASE_NOT_FOUND_MESSAGE) from None

    def for_current(
        self, current: ReleaseKey | None
    ) -> tuple[IndicatorEstimate, ...]:
        if current is None:
            raise ReleaseNotFoundError(RELEASE_NOT_FOUND_MESSAGE)
        return self.get(current)
