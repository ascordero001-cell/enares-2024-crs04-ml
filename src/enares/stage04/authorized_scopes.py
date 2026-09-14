"""Closed, reviewed Stage 04 adapter scopes; contains no institutional values."""

from __future__ import annotations

from .candidate_adapter import CandidateScope

VS_MATRIX_CATEGORIES = (
    "P(con contacto (301 o 302) | no física (303)): de no física (303), % con con contacto (301 o 302)",
    "P(no física (303) | con contacto (301 o 302)): de con contacto (301 o 302), % con no física (303)",
    "P(agresión con contacto (302) | no física (303)): de no física (303), % con agresión con contacto (302)",
    "P(agresión con contacto (302) | violación (301)): de violación (301), % con agresión con contacto (302) [referencial]",
    "P(no física (303) | agresión con contacto (302)): de agresión con contacto (302), % con no física (303)",
    "P(no física (303) | violación (301)): de violación (301), % con no física (303) [referencial]",
    "P(violación (301) | agresión con contacto (302)): de agresión con contacto (302), % con violación (301) [referencial]",
    "P(violación (301) | no física (303)): de no física (303), % con violación (301) [referencial]",
)
VS_MATRIX_PAIRS = frozenset(
    (("2×2", category) if index < 2 else ("3×3", category))
    for index, category in enumerate(VS_MATRIX_CATEGORIES)
)

D06_SCOPE = CandidateScope(
    module_id="3.5",
    indicator_id="Solap_VS_12M",
    allowed_pairs=VS_MATRIX_PAIRS,
    dictionary_type="special",
    output_type="prevalence",
    adapter_id="solap-vs-12m-special-prevalence-v1",
)
D07_SCOPE = CandidateScope(
    module_id="3.5",
    indicator_id="Solap_VS_VIDA",
    allowed_pairs=VS_MATRIX_PAIRS,
    dictionary_type="special",
    output_type="prevalence",
    adapter_id="solap-vs-vida-special-prevalence-v1",
)

D09_PAIRS = frozenset(
    [("Discapacidad", value) for value in ("0", "1")]
    + [("Etnicidad", value) for value in ("1", "3", "5", "6", "9")]
    + [("Idioma del hogar", value) for value in ("1", "3", "4")]
    + [("Nacional", "Total")]
    + [("Sexo", value) for value in ("1", "2")]
    + [("Tipo de hogar", value) for value in ("1", "2", "3")]
    + [("Área", value) for value in ("1", "2")]
    + [
        ("Área × sexo", value)
        for value in ("Rural Hombre", "Rural Mujer", "Urbano Hombre", "Urbano Mujer")
    ]
)
D09_SCOPE = CandidateScope(
    module_id="3.5",
    indicator_id="CONS_ATENCION_SALUD",
    allowed_pairs=D09_PAIRS,
    dictionary_type="prevalence",
    output_type="prevalence",
    adapter_id="cons-atencion-salud-domain-v1",
)
D09_DOMAIN = "CONS_ALGUNA = 1"
