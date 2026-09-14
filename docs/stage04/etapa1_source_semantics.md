# Etapa 1 — verificaciones de fuente D01, D11 y alias D12

Estado: `SOURCE_SEMANTICS_VERIFIED; ADAPTER_SEPARATION_REVIEW_PENDING`

Alcance: documentación y contratos locales; ninguna cifra nueva conectada.

## D01 — significado de `tarea1_fem`–`tarea10_fem`

Fuente lógica contrastada: `07_CRS04_3.1_Caracteristicas_violencia_Percepciones_ver6.sps`,
bloque “Roles de género y división del trabajo en el hogar”, pregunta `C3P302`.

- **Universo:** adolescentes de 12 a 17 años de CRS04 incluidos en la base analítica, con
  respuesta válida al ítem `C3P302` correspondiente.
- **Sujeto que informa:** la/el adolescente entrevistada/o comunica quién realiza principalmente
  cada tarea del hogar o de cuidado.
- **Persona de referencia de `_fem`:** madre, hermana u otra mujer. La/el adolescente
  entrevistada/o es una categoría separada en los ítems 1–7; “nadie” es una categoría separada
  en los ítems 8–10.
- **Regla:** cada `tarea*_fem` vale 1 cuando la categoría resumida es “Principalmente mujer” y 0
  cuando la tarea válida corresponde a otra categoría. No significa que la entrevistada sea mujer
  ni que ella realice la tarea.

Las diez tareas, en orden, son: Cocinar; Lavar/planchar ropa; Compras mercado; Dar
dinero/gastos; Limpieza; Lavar platos/utensilios; Cuidar hermanas/os; Ayudar con tareas
escolares; Aconsejar y escuchar; Jugar contigo.

## D11 — `C3P213 == 5`

Fuente lógica contrastada: `12_CRS03_CRS04_3.6_BusquedaAyuda_Hogar_Escuela_ver5.sps`, bloque
“Razón por la que no recibió ayuda”.

- Pregunta fuente: “¿Por qué crees que no te ayudó / ayudaron?”.
- Valor objetivo exacto: `5`.
- Etiqueta exacta del valor: **No supieron cómo ayudarme**.
- Texto de presentación registrado: **No recibió ayuda porque no supieron cómo ayudarle**.
- Dominio/denominador registrado: `dom_no_recibio_hogar == 1`.
- Alcance: únicamente `C3P213`, Nacional / Total; no crea una regla binaria general.

## D12 — etiquetas de presentación y trazabilidad

La interfaz usa siempre **Área × sexo** e **Idioma del hogar**. El contrato
`presentation.py` devuelve esas mismas etiquetas para tarjeta, tabla, gráfico, tooltip,
impresión y exportación. La metadata conserva, sin mostrarlos como etiquetas de interfaz:

| Etiqueta UI | Nombre fuente | Código fuente |
|---|---|---|
| Área × sexo | Área y sexo | `AREA BY SEXO` |
| Idioma del hogar | Lengua materna | `idiomaHogar` |

Los alias no amplían indicadores, dimensiones ni categorías autorizadas.

## Punto de parada: separación de adaptadores

Se prepararon dos fronteras incompatibles en `adapter_boundaries.py`; la propuesta completa está
en [adapter_separation_review.md](adapter_separation_review.md):

1. `SyntheticCandidateAdapter` reutiliza la barrera existente y acepta únicamente filas con
   `synthetic=true`. Su alcance es prueba local.
2. `InstitutionalAuthorizedAggregateAdapter` exige `synthetic=false`, tiene identidad y versión
   propias y permanece en `REVIEW_REQUIRED_BEFORE_FIRST_AGGREGATE`. Su método de adaptación se
   detiene deliberadamente antes de transformar datos.

La aplicación no importa ni instancia el adaptador institucional. Ningún dato real se marca como
sintético y ningún agregado nuevo se conecta antes de la revisión supervisora de esta separación.
