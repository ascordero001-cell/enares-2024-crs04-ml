"""Application-facing aliases for the single Stage 04 module registry."""

from enares.stage04.modules import DIMENSIONS, MODULES, get_module, module_for_page


NAVIGATION = (
    "Resumen",
    *(module.page_label for module in MODULES),
    "Metodología",
    "Estado del release",
)

FUTURE_DIMENSIONS = DIMENSIONS

SUPPORTED_FILTER = ("Nacional", "Total")

QUALITY_LABELS = {
    "PUBLISHABLE_CANDIDATE": "Candidato — revisión pendiente",
    "REFERENCE_HIGH_CV": "Referencial — precisión limitada",
    "SUPPRESSED_EXERCISE": "Suprimido — confidencialidad protegida",
}
