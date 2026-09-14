"""Source-verified semantics required before Stage 04 adapter integration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HouseholdTaskFemaleSemantic:
    variable: str
    task: str
    display_label: str


@dataclass(frozen=True)
class HouseholdTaskNobodySemantic:
    variable: str
    task: str
    display_label: str


D01_UNIVERSE = (
    "Adolescentes de 12 a 17 años de CRS04 incluidos en la base analítica, "
    "con respuesta válida al ítem C3P302 correspondiente"
)
D01_REPORTING_SUBJECT = (
    "La/el adolescente entrevistada/o informa quién realiza la tarea"
)
D01_FEMALE_REFERENCE = ("Madre", "Hermana", "Otra mujer")
D01_TASKS = (
    HouseholdTaskFemaleSemantic(
        "tarea1_fem",
        "Cocinar",
        "Porcentaje en que cocinar la realiza principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea2_fem",
        "Lavar/planchar ropa",
        "Porcentaje en que lavar o planchar ropa la realiza principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea3_fem",
        "Compras mercado",
        "Porcentaje en que hacer las compras del mercado la realiza principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea4_fem",
        "Dar dinero/gastos",
        "Porcentaje en que aportar dinero para los gastos la realiza principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea5_fem",
        "Limpieza",
        "Porcentaje en que la limpieza la realiza principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea6_fem",
        "Lavar platos/utensilios",
        "Porcentaje en que lavar platos o utensilios la realiza principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea7_fem",
        "Cuidar hermanas/os",
        "Porcentaje en que cuidar a hermanas o hermanos la realiza principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea8_fem",
        "Ayudar con tareas escolares",
        "Porcentaje en que quien ayuda con las tareas escolares es principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea9_fem",
        "Aconsejar y escuchar",
        "Porcentaje en que quien aconseja y escucha es principalmente una mujer del hogar",
    ),
    HouseholdTaskFemaleSemantic(
        "tarea10_fem",
        "Jugar contigo",
        "Porcentaje en que quien juega con ella es principalmente una mujer del hogar",
    ),
)
D01_TASK_EXECUTION_GROUP = D01_TASKS[:7]
D01_RELATIONSHIP_GROUP = D01_TASKS[7:]
D01_NOBODY_SERIES = (
    HouseholdTaskNobodySemantic(
        "tarea8_nadie",
        "Ayudar con tareas escolares",
        "Porcentaje de adolescentes con quienes nadie ayuda con las tareas escolares",
    ),
    HouseholdTaskNobodySemantic(
        "tarea9_nadie",
        "Conversar y escuchar",
        "Porcentaje de adolescentes con quienes nadie conversa y escucha",
    ),
    HouseholdTaskNobodySemantic(
        "tarea10_nadie", "Jugar", "Porcentaje de adolescentes con quienes nadie juega"
    ),
)
D01_NOBODY_DENOMINATOR = "n_tareas_validas_8_10"
D01_EXCLUDED_INDICATORS = frozenset({"predominio_femenino_tareas"})

C3P213_TARGET_VALUE = 5
C3P213_TARGET_VALUE_LABEL = "No supieron cómo ayudarme"
C3P213_DISPLAY_LABEL = "No recibió ayuda porque no supieron cómo ayudarle"
C3P213_DOMAIN = "dom_no_recibio_hogar == 1"
