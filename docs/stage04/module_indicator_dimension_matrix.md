# Matriz módulo × indicador × dimensión — Etapa 1 conectada

Estado: `AUTHORIZED_ETAPA1_LOCAL_SHADOW`.

Esta matriz registra lo que la aplicación local puede leer después de validar CSV,
manifiesto, SHA-256 del extracto, SHA-256 del padre y registro V0. No autoriza
publicación, exportación, cutover ni recursos cloud.

| Módulo | Indicador | Alcance conectado | Filas | Comportamiento local |
|---|---|---|---:|---|
| 3.1 | `Componentes` | `Tareas del hogar`: diez tareas autorizadas | 10 | Dos tablas estáticas: ítems 1–7 e ítems 8–10; sin descarga |
| 3.2 | `VF_HOGAR` | Nacional / Total | 1 | Golden autorizado, sin cambios |
| 3.3 | `C3P223_10_1` | Nacional / Total | 1 | Tarjeta individual validada |
| 3.4 | `Agresor_VS_12M__AG_01` | Nacional / Total | 1 | Tarjeta individual validada |
| 3.5 | `CONS_ATENCION_SALUD` | 22 pares exactos en ocho dimensiones, sin Departamento | 22 | Dominio `CONS_ALGUNA = 1` visible; CV/N no suprimen |
| 3.6 | `C3P213` | Nacional / Total | 1 | Tarjeta individual; valor 5 y dominio documentados |

## Pares conectados de D09

| Dimensión | Categorías |
|---|---|
| Nacional | Total |
| Sexo | 1, 2 |
| Área | 1, 2 |
| Área × sexo | Rural Hombre, Rural Mujer, Urbano Hombre, Urbano Mujer |
| Idioma del hogar | 1, 3, 4 |
| Discapacidad | 0, 1 |
| Etnicidad | 1, 3, 5, 6, 9 |
| Tipo de hogar | 1, 2, 3 |

Los alias D12 se aplican en la interfaz sin alterar los nombres fuente. Las etiquetas
aprobadas de las categorías codificadas se resuelven en presentación. Trece de las 22
celdas D09 tienen CV superior a 15 % y permanecen visibles como referenciales.

## Exclusiones y parada segura

- D01 no incluye `predominio_femenino_tareas` ni las tres series «nadie».
- D09 no incluye Departamento.
- La política de confidencialidad fue aprobada sin umbral de recuento. D06 y D07 pueden conectarse
  mediante un PR posterior, sin cruces nuevos ni granularidad más fina que V0.
- D06 y D07 se conectaron como dos matrices independientes de ocho filas, en estado
  `SUPERVISORY_REVIEW_PENDING`; los cruces 2×2 y 3×3 se validan contra el catálogo V0 en la ruta
  ejecutable.
- Las combinaciones ausentes devuelven «sin datos» y nunca se fabrican.
- Exportación permanece deshabilitada y `BigQueryRepository` sigue bloqueado.
- Cloud: `NOT_AUTHORIZED`; presupuesto máximo registrado: USD 20 mensuales en total.

Pruebas: `tests/test_stage04_etapa1_connection.py`, suite general y golden 3.2.
