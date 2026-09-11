"""Single metadata registry for the six local Stage 04 modules."""

from __future__ import annotations

from dataclasses import dataclass


DIMENSIONS = (
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

LOCAL_COVERAGE_RUN_ID = "sprint042-corte2-local-coverage-001"
AUTHORIZED_GOLDEN = "AUTHORIZED_GOLDEN"
PENDING_QUALITY_SUPPRESSION = "PENDING_QUALITY_SUPPRESSION"


@dataclass(frozen=True)
class ModuleDefinition:
    module_id: str
    label: str
    order: int
    indicator_ids: tuple[str, ...]
    universe: str
    denominator: str
    available_dimensions: tuple[str, ...]
    authorized_dimensions: tuple[str, ...]
    data_state: str

    @property
    def page_label(self) -> str:
        return f"Módulo {self.module_id}"

    @property
    def full_label(self) -> str:
        return f"{self.module_id} {self.label}"


MODULES = (
    ModuleDefinition(
        "3.1",
        "Mitos sobre el castigo",
        1,
        ("justifica_castigo_parental", "justifica_castigo_docente"),
        "Adolescentes de CRS04 con respuesta válida según el indicador; ENARES 2024",
        "casos válidos del diseño muestral",
        DIMENSIONS,
        (),
        PENDING_QUALITY_SUPPRESSION,
    ),
    ModuleDefinition(
        "3.2",
        "Violencia en el hogar",
        2,
        ("VF_HOGAR",),
        "Adolescentes de 12 a 17 años de CRS04 con VF_HOGAR válido; ENARES 2024",
        "casos válidos del diseño muestral",
        DIMENSIONS,
        ("Nacional",),
        AUTHORIZED_GOLDEN,
    ),
    ModuleDefinition(
        "3.3",
        "Violencia en la escuela",
        3,
        ("C3P223_10_1",),
        "Adolescentes de 12 a 17 años con VP_ESCUELA == 1; ENARES 2024",
        "VP_ESCUELA == 1",
        ("Nacional",),
        (),
        PENDING_QUALITY_SUPPRESSION,
    ),
    ModuleDefinition(
        "3.4",
        "Violencia sexual",
        4,
        ("Agresor_VS_12M__AG_01",),
        "Adolescentes de 12 a 17 años con VS_12M == 1; ENARES 2024",
        "VS_12M == 1",
        ("Nacional",),
        (),
        PENDING_QUALITY_SUPPRESSION,
    ),
    ModuleDefinition(
        "3.5",
        "Acumulación de violencia",
        5,
        ("PV_hogar_escuela",),
        "Adolescentes de 12 a 17 años con respuesta válida; ENARES 2024",
        "casos válidos del diseño muestral",
        DIMENSIONS,
        (),
        PENDING_QUALITY_SUPPRESSION,
    ),
    ModuleDefinition(
        "3.6",
        "Búsqueda de ayuda",
        6,
        ("C3P213",),
        "Adolescentes de 12 a 17 años con dom_no_recibio_hogar == 1; ENARES 2024",
        "dom_no_recibio_hogar == 1",
        ("Nacional",),
        (),
        PENDING_QUALITY_SUPPRESSION,
    ),
)

MODULE_BY_ID = {module.module_id: module for module in MODULES}
MODULE_BY_PAGE = {module.page_label: module for module in MODULES}


def get_module(module_id: str) -> ModuleDefinition:
    try:
        return MODULE_BY_ID[module_id]
    except KeyError as error:
        raise ValueError(f"Unknown Stage 04 module: {module_id}") from error


def module_for_page(page_label: str) -> ModuleDefinition | None:
    return MODULE_BY_PAGE.get(page_label)
