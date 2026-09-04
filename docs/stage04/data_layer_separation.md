# Separación local de capas de datos

- `outputs` conserva el historial completo e inmutable de resultados candidatos y sus estados.
- `published` ofrece una superficie reducida y segura: solo agregados aprobados y supresión
  aplicada antes del consumo.
- `ops` registra corridas, validaciones, promoción, release vigente y rollback.

La separación evita que una aplicación confunda “calculado” con “aprobado”. Un candidato pasa a
`published` únicamente después de controles automáticos, revisión supervisora y promoción en
`ops`. Si una promoción es incorrecta, rollback mueve el puntero al release aprobado anterior;
no borra ni reescribe resultados.

La aplicación nunca consulta CSV privados ni `survey_input`: esos artefactos tienen más detalle,
no expresan por sí solos una decisión de publicación y no son una interfaz estable. En esta fase
solo existe una implementación local sobre fixtures sintéticos o agregados autorizados. Cualquier
repositorio BigQuery permanece como diseño no conectado y `BLOCKED_BY_CLOUD_GATE`.
