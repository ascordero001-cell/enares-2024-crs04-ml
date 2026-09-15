# Modelo de amenazas — Stage 04 controlled shadow

- Fecha de actualización: 2026-09-14 UTC
- Estado: `CONTROLLED_SHADOW_GO; DEPLOYMENT_NOT_STARTED`
- Datos: solo agregados V0 aprobados; nunca microdatos
- Publicación institucional y cutover: `NOT_AUTHORIZED`
- Recursos cloud: bloqueados hasta verificar privadamente proyecto y cuenta de billing

Este modelo aplica a la aplicación, exportaciones, caché, logs y acceso directo. La regla de
confidencialidad vigente es el límite de granularidad aprobado en el PR #66: Stage 04 no muestra
cortes más finos que V0 ni fabrica cruces ausentes de los tabulados oficiales.

## Activos y fronteras

| Activo o frontera | Control vigente |
|---|---|
| Agregado institucional V0 | Procedencia ligada a manifiesto, SHA-256 y registro aprobado |
| Aplicación Streamlit | Servicio autenticado, sin acceso público y con máximo una instancia |
| Datos visibles | Solo filas autorizadas tras validación fail-closed y diagnóstico de release |
| BigQuery futuro | La identidad de ejecución solo podrá consultar `published`; sin acceso a capas previas |
| Exportaciones | Deben reproducir V0 y sus notas de CV/N; no crean cruces ni granularidad nueva |
| Caché y logs | No deben conservar valores anteriores a la frontera validada ni principales privados |
| Identidades | Seis personas aprobadas; los principales exactos se verifican por canal privado |

## Amenazas y mitigaciones

| Amenaza | Mitigación obligatoria | Evidencia requerida |
|---|---|---|
| Acceso anónimo o de una identidad no autorizada | Cloud Run sin `allUsers`/`allAuthenticatedUsers`; `run.invoker` solo para las seis identidades aprobadas | Pruebas negativa y positiva posteriores al GO |
| Lectura de microdatos o archivos `.sav` | Imagen runtime sin `pyreadstat`, Drive ni clientes de datos no utilizados; repositorio institucional acepta únicamente agregados con procedencia verificada | CI del contenedor y pruebas de repositorio |
| Consulta de capas anteriores a `published` | Cuenta de ejecución con `dataViewer` solo en `published` y `jobUser` en el proyecto | Prueba IAM positiva sobre `published` y negativa sobre las demás capas |
| Exposición mediante enlace o descarga directa | Todas las rutas y descargas heredan autenticación; no existen endpoints públicos alternos | Verificación directa de rutas y archivos |
| Escalada o permanencia tras una baja | Ana aplica/revoca; Rita revisa cada binding; sin claves JSON | Evidencia de revocación efectiva y registro UTC |
| Release mezclado o incompleto | Diagnóstico exige un `release_id`, un `source_version` y módulos 3.1–3.6 no vacíos | Health profundo y CI del contenedor |
| Consulta o coste fuera de control | `maximum_bytes_billed`, cuota diaria BigQuery, Cloud Run min=0/max=1 y una imagen viva | Configuración capturada después de la verificación privada |
| Inyección de fórmulas en exportaciones | Escapar celdas que comiencen con caracteres de fórmula y validar el paquete OOXML | Pruebas sintéticas de exportación |

## Confidencialidad estadística vigente

No existe supresión primaria por recuento. `CV > 15 %` y `base_unw < 30` producen alertas
visibles, nunca supresión. Una celda con un caso no identifica por sí sola a una persona porque V0
no baja de departamento ni contiene escuela, distrito, conglomerado o identificación nominal.

La maquinaria de supresión complementaria, márgenes, multitabla y multirelease se conserva y se
prueba, pero permanece inactiva. Solo podrá activarse tras una nueva decisión supervisora si se
autoriza un corte más fino que departamento o un cruce ausente de V0. Una cifra publicada se
considera permanentemente expuesta aunque un release deje de estar accesible.

## Riesgo residual y condiciones de parada

El riesgo residual principal es una configuración IAM incorrecta, una ruta de descarga que eluda
la autenticación o una ampliación accidental de granularidad. Cualquiera de estos hallazgos detiene
la prueba: no se publica, se revoca el acceso o se restaura la revisión previa y se registra el
evento. El GO vigente autoriza configurar y verificar; no autoriza publicar cifras.

La plantilla operativa está en [access_verification.md](access_verification.md) y el reparto de
roles en [access_control_plan.md](access_control_plan.md).
