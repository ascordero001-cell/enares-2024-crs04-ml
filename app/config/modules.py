"""Labels and filter capabilities; no estimates or methodological rules live here."""

NAVIGATION = ("Resumen", "Módulo 3.2", "Metodología", "Estado del release")

FUTURE_DIMENSIONS = (
    "Nacional",
    "Sexo",
    "Área",
    "Área × sexo",
    "Idioma del hogar",
    "Discapacidad",
    "Etnicidad",
    "Tipo de hogar",
    "Departamento",
)

SUPPORTED_FILTER = ("Nacional", "Total")

QUALITY_LABELS = {
    "PUBLISHABLE_CANDIDATE": "Candidato — revisión pendiente",
    "REFERENCE_HIGH_CV": "Referencial — precisión limitada",
    "SUPPRESSED_EXERCISE": "Suprimido — confidencialidad protegida",
}
