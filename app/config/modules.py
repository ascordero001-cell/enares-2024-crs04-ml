"""Application-facing aliases for the single Stage 04 module registry."""

from enares.stage04.modules import DIMENSIONS, MODULES

NAVIGATION = (
    "Resumen",
    *(module.page_label for module in MODULES),
    "Metodología",
    "Estado del release",
)

FUTURE_DIMENSIONS = DIMENSIONS

SUPPORTED_FILTER = ("Nacional", "Total")

QUALITY_LABELS = {
    "CONTEXT_ONLY": "Contexto V0 — sin métrica inferencial",
    "EXACT_ZERO_CV_UNDEFINED": "Cero observado — CV indefinido",
    "PUBLISHABLE_CANDIDATE": "Candidato — revisión pendiente",
    "REFERENCE_HIGH_CV": "Referencial — precisión limitada",
    "SUPPRESSED_EXERCISE": "Suprimido — confidencialidad protegida",
}
