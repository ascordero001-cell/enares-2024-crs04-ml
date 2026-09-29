"""Supervisor-approved Stage 04 report topics, without numerical transformations.

Source: issue #149, comment 5817515558. Topic IDs are presentation-only;
indicator IDs and the approved release remain unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass

MODULE_NAMES = {
    "3.1": "Percepciones",
    "3.2": "Violencia en el hogar",
    "3.3": "Violencia en el entorno escolar",
    "3.4": "Violencia sexual",
    "3.5": "Acumulación de violencias",
    "3.6": "Ayuda y respuesta",
}

TOPIC_TITLES = {
    "3.1": (
        "Normalizan que madre o padre golpeen para corregir.",
        "Normalizan que docentes golpeen para corregir.",
        "Rechazan que niñas, niños y adolescentes deban trabajar cuando falta dinero en casa.",
        "Reconocen el derecho a opinar y expresar lo que piensan o sienten.",
        "Rechazan que madre o padre decidan que su hija o hijo deje de estudiar.",
        "Reconocen el derecho a denunciar a quien los lastima.",
        "Identifican el predominio femenino en la realización de tareas del hogar.",
        "Creen que la violencia sexual solo la cometen personas “locas”.",
        "Creen que la violencia sexual solo les ocurre a niñas, niños y adolescentes pobres.",
        "Creen que la violencia sexual ocurre mayormente fuera de la casa.",
        "Creen que la violencia sexual ocurre más en sitios oscuros y solitarios.",
    ),
    "3.2": (
        "Violencia psicológica ejercida en el hogar por madre, padre o cuidadores.",
        "Formas de violencia psicológica en el hogar y tipo de agresor.",
        "Violencia física ejercida en el hogar por madre, padre o cuidadores.",
        "Formas de violencia física en el hogar y tipo de agresor.",
        "Violencia sexual ejercida por familiares en el hogar.",
        "Formas de violencia sexual por familiares y sexo del agresor.",
        "Situaciones de negligencia física en el hogar.",
        "Negligencia: haber sido dejada o dejado sin comer por un día o más.",
        "Negligencia: falta de supervisión o abandono en el hogar.",
        "Situaciones de riesgo personales e inducidas por cuidadores.",
        "Violencia psicológica y/o física y/o negligencia en el hogar.",
        "Violencia psicológica y/o física en el hogar.",
        "Violencia psicológica y física en el hogar.",
        "Coexistencia de violencia psicológica y violencia física en el hogar.",
        "Violencia psicológica, física y sexual en el hogar.",
        "Violencia psicológica y/o física y/o sexual en el hogar.",
        "Diferencia en la prevalencia de violencia psicológica en el hogar frente a la categoría de referencia.",
        "Diferencia en la prevalencia de violencia física en el hogar frente a la categoría de referencia.",
    ),
    "3.3": (
        "Víctimas de violencia psicológica por parte de un compañero u otro estudiante.",
        "Formas de violencia psicológica escolar y tipos de agresor.",
        "Víctimas de violencia física por parte de un compañero u otro estudiante.",
        "Formas de violencia física escolar y tipos de agresor.",
        "Víctimas de violencia sexual por parte de un compañero u otro estudiante.",
        "Formas de violencia sexual escolar reportadas por las víctimas.",
        "Víctimas de violencia psicológica y física en la escuela.",
        "Víctimas de violencia psicológica y/o física en la escuela.",
        "Víctimas de violencia psicológica y/o física y/o sexual en la escuela.",
        "Víctimas de violencia psicológica, física y sexual en la escuela.",
        "Solapamiento de violencia psicológica y física en la escuela.",
        "Lugar y horario de la violencia psicológica y/o física escolar.",
        "Ejercen violencia psicológica contra un compañero u otro estudiante.",
        "Ejercen violencia física contra un compañero u otro estudiante.",
        "Ejercen violencia psicológica y/o física en la escuela.",
        "Formas de violencia escolar ejercidas por niñas, niños y adolescentes.",
        "Caracterización de la violencia psicológica recibida en la escuela.",
        "Caracterización de la violencia física recibida en la escuela.",
        "Caracterización de la violencia psicológica ejercida en la escuela.",
        "Caracterización de la violencia física ejercida en la escuela.",
    ),
    "3.4": (
        "Reportaron al menos una situación de violencia sexual.",
        "Formas de violencia sexual reportadas por las víctimas.",
        "Tipo de agresor o agresora de la violencia sexual.",
        "Coincidencia entre formas ICVAC de violencia sexual.",
        "Violencia sexual ejercida por otra persona.",
        "Violencia sexual ejercida por un agresor distinto a la pareja.",
        "Violencia sexual antes de los 12 años.",
        "Acoso sexual ejercido por un agresor distinto a la pareja.",
        "Caracterización de la violencia sexual frente a las categorías de referencia.",
    ),
    "3.5": (
        "Violencia psicológica y/o física en el hogar y en la escuela.",
        "Violencia psicológica en el hogar y en la escuela.",
        "Violencia física en el hogar y en la escuela.",
        "Violencia psicológica en el hogar y violencia física en la escuela.",
        "Violencia física en el hogar y violencia psicológica en la escuela.",
        "Violencia psicológica y física en el hogar y en la escuela.",
        "Violencia psicológica, física y/o sexual en el hogar y en la escuela.",
        "Violencia psicológica y física en el hogar y la escuela, y violencia sexual.",
        "Concurrencia de violencia entre el hogar y la escuela.",
        "Consecuencias físicas asociadas al maltrato en el hogar/CAR o colegio.",
        "Atención en salud por consecuencias físicas del maltrato.",
        "Número y tipo de consecuencias físicas y atención en salud.",
    ),
    "3.6": (
        "Recorrido de búsqueda y recepción de ayuda frente a la violencia en el hogar.",
        "Recorrido de búsqueda y recepción de ayuda frente a la violencia en la escuela.",
        "Recorrido de búsqueda y recepción de ayuda frente a la violencia sexual.",
        "Persona a la que pidió ayuda frente a la violencia en el hogar.",
        "Persona a la que pidió ayuda frente a la violencia en la escuela.",
        "Persona a la que pidió ayuda frente a la violencia sexual.",
        "Ayuda recibida de una persona cercana frente a la violencia.",
        "Razones por las que no recibió ayuda de la persona a la que acudió.",
        "Institución a la que acudió por violencia en el hogar o en la escuela.",
        "Institución a la que acudió por violencia sexual, ayuda recibida y conocimiento de la DEMUNA.",
    ),
}


@dataclass(frozen=True)
class ReportTopic:
    module_id: str
    number: int
    title: str

    @property
    def topic_id(self) -> str:
        return f"{self.module_id}.{self.number}"


REPORT_TOPICS = tuple(
    ReportTopic(module_id, number, title)
    for module_id, titles in TOPIC_TITLES.items()
    for number, title in enumerate(titles, start=1)
)
