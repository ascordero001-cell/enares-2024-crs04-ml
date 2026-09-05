# Contrato local de operaciones y releases

- Estado: `CANDIDATE_LOCAL_SHADOW`
- Cloud: `BLOCKED_BY_CLOUD_GATE`

## Entidades conceptuales

| Entidad | Propósito | Campos mínimos |
|---|---|---|
| `pipeline_runs` | Una fila por ejecución, exitosa o fallida | `run_id`, `release_id`, fuente, commit, inicio, fin, estado |
| `validation_results` | Resultado auditable de cada control | `run_id`, control, estado, evidencia, fecha |
| `current_release` | Puntero único al release visible | `release_id`, aprobación, fecha de promoción, versión anterior |

## Estados

- `PENDING`: recibido, aún no validado por completo.
- `PASSED`: controles automáticos superados; todavía no implica aprobación supervisora.
- `FAILED`: uno o más controles bloqueantes fallaron.
- `APPROVED`: validación y decisión supervisora registradas.

## Promoción y rollback

La promoción verifica que el release está `APPROVED`, conserva el puntero anterior y cambia
atómicamente `current_release`. `current_release` nunca apunta a `PENDING`, `PASSED` sin
aprobación o `FAILED`. El rollback restaura el último puntero aprobado sin borrar historial,
registra quién lo decidió y conserva la corrida defectuosa para auditoría.

No se ejecuta DDL ni se crea infraestructura: toda operación cloud está
`BLOCKED_BY_CLOUD_GATE`.
