"""Measure the seven frozen synthetic C0 catalog-location tasks."""

from __future__ import annotations

import statistics
import sys
from pathlib import Path
from time import perf_counter_ns

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from enares.stage04.catalog_navigation import CatalogLocator, filter_catalog

LOCATORS = (
    CatalogLocator("3.1", "SYN_C0_31_001", "Normas repetidas sobre cuidado (hogar)", "Nacional", "Total"),
    CatalogLocator("3.2", "SYN_C0_32_001", "Violencia física en el hogar: episodio repetido (12 meses)", "Nacional", "Total"),
    CatalogLocator("3.3", "SYN_C0_33_001", "Violencia psicológica en la escuela: episodio repetido (12 meses)", "Nacional", "Total"),
    CatalogLocator("3.4", "SYN_C0_34_001", "Situación sintética de violencia sexual (alguna vez)", "Nacional", "Total"),
    CatalogLocator("3.5", "SYN_C0_35_001", "Consecuencias físicas acumuladas (tres o más)", "Nacional", "Total"),
    CatalogLocator("3.6", "SYN_C0_36_001", "Búsqueda de ayuda después de un episodio (persona adulta)", "Nacional", "Total"),
    CatalogLocator("3.2", "SYN_C0_DEP_001", "Violencia física en el hogar: episodio repetido (12 meses)", "Departamento", "Departamento sintético 07"),
)
TASKS = (
    ("C0-01", "3.1", "Nacional", "cuidado hogar", "SYN_C0_31_001"),
    ("C0-02", "3.2", "Nacional", "fisica 12 meses", "SYN_C0_32_001"),
    ("C0-03", "3.3", "Nacional", "psicologica escuela 12 meses", "SYN_C0_33_001"),
    ("C0-04", "3.4", "Nacional", "sexual alguna vez", "SYN_C0_34_001"),
    ("C0-05", "3.5", "Nacional", "consecuencias tres", "SYN_C0_35_001"),
    ("C0-06", "3.6", "Nacional", "ayuda persona adulta", "SYN_C0_36_001"),
    ("C0-07", "3.2", "Departamento", "fisica sintetico 07", "SYN_C0_DEP_001"),
)


def main() -> None:
    print("task,module,dimension,query,median_ms,result")
    for task_id, module_id, dimension, query, expected in TASKS:
        samples = []
        result = ()
        for _ in range(1000):
            start = perf_counter_ns()
            result = filter_catalog(
                LOCATORS, module_id=module_id, dimension=dimension, query=query
            )
            samples.append((perf_counter_ns() - start) / 1_000_000)
        status = "PASS" if [row.indicator_id for row in result] == [expected] else "FAIL"
        print(
            f'{task_id},{module_id},{dimension},"{query}",'
            f"{statistics.median(samples):.6f},{status}"
        )


if __name__ == "__main__":
    main()
