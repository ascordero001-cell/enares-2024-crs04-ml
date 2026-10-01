from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

MODULE_IDS = ("3.1", "3.2", "3.3", "3.4", "3.5", "3.6")
EXPECTED_COUNTS = {"3.1": 11, "3.2": 18, "3.3": 20, "3.4": 9, "3.5": 12, "3.6": 10}
EXPECTED_INDICATOR_COUNT = 516
EXPECTED_ROW_COUNT = 3014
STANDARD_SCOPE = "ESTANDAR"
STANDARD_DISAGGREGATIONS = frozenset(
    {
        "Nacional",
        "Departamento",
        "Área",
        "Sexo",
        "Área × sexo",
        "Idioma del hogar",
        "Etnicidad",
        "Tipo de hogar",
        "Discapacidad",
    }
)
VALID_PERIOD_LABELS = frozenset(
    {
        "Últimos 12 meses",
        "Alguna vez en la vida",
        "Antes de los 12 años",
        "No aplica",
    }
)
# Solo se agrega un tema con evidencia en el PR de que V0 no tiene filas para él.
TOPICS_WITHOUT_V0_DATA: frozenset[str] = frozenset(
    {
        "3.2.09",  # No distinct supervision/abandonment estimate in this release.
        "3.3.17",  # No VP_ESCUELA characterisation rows in this release.
        "3.3.18",  # No VF_ESCUELA characterisation rows in this release.
    }
)

TOPIC_TITLES: dict[str, tuple[str, ...]] = {
    "3.1": (
        "Normalizan que madre o padre golpeen para corregir",
        "Normalizan que docentes golpeen para corregir",
        "Rechazan que niñas, niños y adolescentes deban trabajar cuando falta dinero en casa",
        "Reconocen el derecho a opinar y expresar lo que piensan o sienten",
        "Rechazan que madre o padre decidan que su hija o hijo deje de estudiar",
        "Reconocen el derecho a denunciar a quien los lastima",
        "Identifican el predominio femenino en la realización de tareas del hogar",
        "Creen que la violencia sexual solo la cometen personas “locas”",
        "Creen que la violencia sexual solo les ocurre a niñas, niños y adolescentes pobres",
        "Creen que la violencia sexual ocurre mayormente fuera de la casa",
        "Creen que la violencia sexual ocurre más en sitios oscuros y solitarios",
    ),
    "3.2": (
        "Violencia psicológica ejercida en el hogar por madre, padre o cuidadores",
        "Formas de violencia psicológica en el hogar y tipo de agresor",
        "Violencia física ejercida en el hogar por madre, padre o cuidadores",
        "Formas de violencia física en el hogar y tipo de agresor",
        "Violencia sexual ejercida por familiares en el hogar",
        "Formas de violencia sexual por familiares y sexo del agresor",
        "Situaciones de negligencia física en el hogar",
        "Negligencia: haber sido dejada o dejado sin comer por un día o más",
        "Negligencia: falta de supervisión o abandono en el hogar",
        "Situaciones de riesgo personales e inducidas por cuidadores",
        "Violencia psicológica y/o física y/o negligencia en el hogar",
        "Violencia psicológica y/o física en el hogar",
        "Violencia psicológica y física en el hogar",
        "Coexistencia de violencia psicológica y violencia física en el hogar",
        "Violencia psicológica, física y sexual en el hogar",
        "Violencia psicológica y/o física y/o sexual en el hogar",
        "Diferencia en la prevalencia de violencia psicológica en el hogar frente a la categoría de referencia",
        "Diferencia en la prevalencia de violencia física en el hogar frente a la categoría de referencia",
    ),
    "3.3": (
        "Víctimas de violencia psicológica por parte de un compañero u otro estudiante",
        "Formas de violencia psicológica escolar y tipos de agresor",
        "Víctimas de violencia física por parte de un compañero u otro estudiante",
        "Formas de violencia física escolar y tipos de agresor",
        "Víctimas de violencia sexual por parte de un compañero u otro estudiante",
        "Formas de violencia sexual escolar reportadas por las víctimas",
        "Víctimas de violencia psicológica y física en la escuela",
        "Víctimas de violencia psicológica y/o física en la escuela",
        "Víctimas de violencia psicológica y/o física y/o sexual en la escuela",
        "Víctimas de violencia psicológica, física y sexual en la escuela",
        "Solapamiento de violencia psicológica y física en la escuela",
        "Lugar y horario de la violencia psicológica y/o física escolar",
        "Ejercen violencia psicológica contra un compañero u otro estudiante",
        "Ejercen violencia física contra un compañero u otro estudiante",
        "Ejercen violencia psicológica y/o física en la escuela",
        "Formas de violencia escolar ejercidas por niñas, niños y adolescentes",
        "Caracterización de la violencia psicológica recibida en la escuela",
        "Caracterización de la violencia física recibida en la escuela",
        "Caracterización de la violencia psicológica ejercida en la escuela",
        "Caracterización de la violencia física ejercida en la escuela",
    ),
    "3.4": (
        "Reportaron al menos una situación de violencia sexual",
        "Formas de violencia sexual reportadas por las víctimas",
        "Tipo de agresor o agresora de la violencia sexual",
        "Coincidencia entre formas ICVAC de violencia sexual",
        "Violencia sexual ejercida por otra persona",
        "Violencia sexual ejercida por un agresor distinto a la pareja",
        "Violencia sexual antes de los 12 años",
        "Acoso sexual ejercido por un agresor distinto a la pareja",
        "Caracterización de la violencia sexual frente a las categorías de referencia",
    ),
    "3.5": (
        "Violencia psicológica y/o física en el hogar y en la escuela",
        "Violencia psicológica en el hogar y en la escuela",
        "Violencia física en el hogar y en la escuela",
        "Violencia psicológica en el hogar y violencia física en la escuela",
        "Violencia física en el hogar y violencia psicológica en la escuela",
        "Violencia psicológica y física en el hogar y en la escuela",
        "Violencia psicológica, física y/o sexual en el hogar y en la escuela",
        "Violencia psicológica y física en el hogar y la escuela, y violencia sexual",
        "Concurrencia de violencia entre el hogar y la escuela",
        "Consecuencias físicas asociadas al maltrato en el hogar/CAR o colegio",
        "Atención en salud por consecuencias físicas del maltrato",
        "Número y tipo de consecuencias físicas y atención en salud",
    ),
    "3.6": (
        "Recorrido de búsqueda y recepción de ayuda frente a la violencia en el hogar",
        "Recorrido de búsqueda y recepción de ayuda frente a la violencia en la escuela",
        "Recorrido de búsqueda y recepción de ayuda frente a la violencia sexual",
        "Persona a la que pidió ayuda frente a la violencia en el hogar",
        "Persona a la que pidió ayuda frente a la violencia en la escuela",
        "Persona a la que pidió ayuda frente a la violencia sexual",
        "Ayuda recibida de una persona cercana frente a la violencia",
        "Razones por las que no recibió ayuda de la persona a la que acudió",
        "Institución a la que acudió por violencia en el hogar o en la escuela",
        "Institución a la que acudió por violencia sexual, ayuda recibida y conocimiento de la DEMUNA",
    ),
}

NATIONAL_ONLY = frozenset(
    {
        "3.2.02",
        "3.2.04",
        "3.2.06",
        "3.3.02",
        "3.3.04",
        "3.3.06",
        "3.3.16",
        "3.4.02",
        "3.4.03",
        "3.4.04",
        *(f"3.6.{number:02d}" for number in range(1, 11)),
    }
)

HEADLINE_INDICATOR_BY_MODULE = {
    "3.1": "justifica_castigo_parental",
    "3.2": "VP_HOGAR",
    "3.3": "VP_ESCUELA",
    "3.4": "VS_12M",
    "3.5": "PV_hogar_escuela",
    "3.6": "busco_ayuda_hogar",
}


class TopicCatalogError(RuntimeError):
    pass


class RowKey(Protocol):
    @property
    def indicator_id(self) -> str: ...

    @property
    def disaggregation(self) -> str: ...


@dataclass(frozen=True, slots=True)
class ReportTopic:
    topic_id: str
    module_id: str
    order: int
    title: str
    national_only: bool
    technical_indicator_ids: frozenset[str]


@dataclass(frozen=True, slots=True)
class TopicAssignment:
    module_id: str
    topic_id: str
    indicator_id: str
    disaggregation_scope: str
    period_label: str
    series_label: str
    display_label_override: str


AssignmentIndex = Mapping[tuple[str, str], TopicAssignment]


@dataclass(frozen=True, slots=True)
class TopicCatalog:
    topics: tuple[ReportTopic, ...]
    assignments: AssignmentIndex


def resolve_assignment(assignments: AssignmentIndex, row: RowKey) -> TopicAssignment:
    exact = assignments.get((row.indicator_id, row.disaggregation))
    if exact is not None:
        return exact
    if row.disaggregation in STANDARD_DISAGGREGATIONS:
        standard = assignments.get((row.indicator_id, STANDARD_SCOPE))
        if standard is not None:
            return standard
    raise TopicCatalogError(f"Unmapped row: {row.indicator_id} / {row.disaggregation}")


def _topic_definitions() -> dict[str, tuple[str, int, str]]:
    definitions: dict[str, tuple[str, int, str]] = {}
    for module_id, titles in TOPIC_TITLES.items():
        for order, title in enumerate(titles, start=1):
            topic_id = f"{module_id}.{order:02d}"
            definitions[topic_id] = (module_id, order, title)
    return definitions


def load_topic_mapping(
    path: Path,
    *,
    catalog_rows: Iterable[RowKey],
) -> TopicCatalog:
    definitions = _topic_definitions()
    required_columns = (
        "module_id",
        "report_topic_id",
        "indicator_id",
        "disaggregation_scope",
        "period_label",
        "series_label",
        "display_label_override",
    )
    assignments: dict[tuple[str, str], TopicAssignment] = {}

    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing_columns = set(required_columns) - set(reader.fieldnames or ())
        if missing_columns:
            raise TopicCatalogError(
                f"Missing topic-map columns: {sorted(missing_columns)}"
            )
        for line_number, record in enumerate(reader, start=2):
            values = {column: record[column].strip() for column in required_columns}
            module_id = values["module_id"]
            topic_id = values["report_topic_id"]
            indicator_id = values["indicator_id"]
            scope = values["disaggregation_scope"]
            if not module_id or not topic_id or not indicator_id or not scope:
                raise TopicCatalogError(
                    f"Blank required value at CSV line {line_number}"
                )
            if topic_id not in definitions:
                raise TopicCatalogError(f"Unknown report topic: {topic_id}")
            if definitions[topic_id][0] != module_id:
                raise TopicCatalogError(
                    f"Cross-module presentation mapping: {indicator_id} -> {topic_id}"
                )
            if (indicator_id, scope) in assignments:
                raise TopicCatalogError(
                    f"Duplicate assignment: {indicator_id} / {scope}"
                )
            if values["period_label"] not in VALID_PERIOD_LABELS:
                raise TopicCatalogError(
                    f"Invalid period for {indicator_id}: {values['period_label']!r}"
                )
            assignments[(indicator_id, scope)] = TopicAssignment(
                module_id=module_id,
                topic_id=topic_id,
                indicator_id=indicator_id,
                disaggregation_scope=scope,
                period_label=values["period_label"],
                series_label=values["series_label"],
                display_label_override=values["display_label_override"],
            )

    rows = list(catalog_rows)
    if len(rows) != EXPECTED_ROW_COUNT:
        raise TopicCatalogError(
            f"Expected {EXPECTED_ROW_COUNT} V0 rows, got {len(rows)}"
        )
    if len({row.indicator_id for row in rows}) != EXPECTED_INDICATOR_COUNT:
        raise TopicCatalogError("Unexpected number of technical indicators in V0")

    used: set[tuple[str, str]] = set()
    unmapped: set[tuple[str, str]] = set()
    ids_by_topic: dict[str, set[str]] = {topic_id: set() for topic_id in definitions}
    for row in rows:
        try:
            item = resolve_assignment(assignments, row)
        except TopicCatalogError:
            unmapped.add((row.indicator_id, row.disaggregation))
            continue
        used.add((item.indicator_id, item.disaggregation_scope))
        ids_by_topic[item.topic_id].add(item.indicator_id)

    unused = set(assignments) - used
    empty_topics = {topic_id for topic_id, ids in ids_by_topic.items() if not ids}
    unexpected_empty = empty_topics - TOPICS_WITHOUT_V0_DATA
    declared_with_data = TOPICS_WITHOUT_V0_DATA - empty_topics
    if unmapped or unused or unexpected_empty or declared_with_data:
        raise TopicCatalogError(
            "Invalid topic map; "
            f"unmapped_rows={sorted(unmapped)}, unused_assignments={sorted(unused)}, "
            f"empty_topics={sorted(unexpected_empty)}, "
            f"declared_empty_with_data={sorted(declared_with_data)}"
        )

    topics = tuple(
        ReportTopic(
            topic_id=topic_id,
            module_id=module_id,
            order=order,
            title=title,
            national_only=topic_id in NATIONAL_ONLY,
            technical_indicator_ids=frozenset(ids_by_topic[topic_id]),
        )
        for topic_id, (module_id, order, title) in definitions.items()
    )
    actual_counts = {
        module_id: sum(topic.module_id == module_id for topic in topics)
        for module_id in MODULE_IDS
    }
    if actual_counts != EXPECTED_COUNTS or len(topics) != 80:
        raise TopicCatalogError(f"Unexpected visible catalog: {actual_counts}")
    return TopicCatalog(topics=topics, assignments=assignments)


def topics_for_module(
    topics: Iterable[ReportTopic], module_id: str
) -> tuple[ReportTopic, ...]:
    if module_id not in MODULE_IDS:
        raise TopicCatalogError(f"Invalid module: {module_id}")
    return tuple(
        sorted(
            (topic for topic in topics if topic.module_id == module_id),
            key=lambda topic: topic.order,
        )
    )


def topic_by_id(topics: Iterable[ReportTopic]) -> dict[str, ReportTopic]:
    return {topic.topic_id: topic for topic in topics}
