# Acceso privado del piloto Stage 04

**Decisión supervisora:** issue #149, comentario del 2026-10-13. El acceso
autorizado usa Identity Platform (correo/contraseña), IAP con identidades
externas y un backend Cloud Run privado. El formulario público separado solo
sirve `Usuario`, `Contraseña` e `Ingresar`; traduce el alias visible
`vigilancia` a una identidad interna. No contiene V0 ni puede consultar el
repositorio. La credencial compartida no identifica individualmente a cada
persona usuaria.

El flujo anterior de hash PBKDF2 dentro de Streamlit se retiró. En modo
`AUTHENTICATED_SHADOW`, la aplicación **rechaza antes de abrir V0** una
petición sin JWT firmado por IAP, con audiencia exacta del servicio piloto,
emisor IAP, proveedor Identity Platform `password` y UID aprobado. Ninguna
cabecera de identidad sin firma ni variable de sesión sustituye esa prueba.
La ausencia de configuración falla cerrada.

## Configuración del piloto

- Servicio principal `enares-stage04-shadow`: sin cambios durante el piloto.
- Backend piloto `enares-stage04-iap-pilot`: IAP activo, `roles/run.invoker`
  solo para la cuenta técnica de IAP; nunca `allUsers` ni
  `allAuthenticatedUsers`.
- Servicio de autenticación: imagen aislada de `auth_ui/`, sin código de V0;
  `STAGE04_FIREBASE_API_KEY`, `STAGE04_FIREBASE_AUTH_DOMAIN` y
  `STAGE04_IDP_EMAIL` son configuración pública del cliente, no contraseñas.
  `STAGE04_PILOT_URL` apunta al origen privado al que se vuelve tras cerrar
  la cookie IAP para iniciar un flujo nuevo.
- Backend: `STAGE04_IAP_PROJECT_NUMBER`, `STAGE04_IAP_REGION`,
  `STAGE04_IAP_SERVICE`, `STAGE04_IAP_EXPECTED_UID` y
  `STAGE04_IAP_SERVICE_URL`. El UID debe proceder de la cuenta creada en
  Identity Platform, no de lo que envía el navegador.
- La contraseña debe ser **nueva y fuerte**, administrada en Identity
  Platform y rotada antes del piloto. Nunca se coloca en Git, imagen, logs,
  URLs, variables de entorno visibles ni comentarios. La recuperación se
  realiza mediante el correo interno de la identidad y el flujo de
  restablecimiento de Identity Platform; una rotación revoca la clave anterior.

## Inactividad y verificación

El cliente borra filtros, resultados y estado a los 300 s de inactividad.
El cierre debe terminar la cookie IAP mediante
`?gcp-iap-mode=GCIP_SIGNOUT` y volver al formulario. La política IAP `LOGIN`
con `maxAge=300s` **no cubre identidades externas**, según la documentación
de Google; no se la cuenta como control de este requisito. Hasta comprobar
en navegador el cierre y reingreso obligatorios, el piloto no se promueve.

El formulario utiliza persistencia de credenciales solo en memoria de la
página, no en almacenamiento de sesión ni local. Aplica espera creciente en
el cliente tras tres errores; Identity Platform también dispone de límites
de abuso propios. El servicio de formulario registra únicamente el evento
fijo `stage04_login_denied`, sin usuario, contraseña ni detalle del error.
Ese evento ayuda a investigar fallos del formulario, **pero no es un contador
autoritativo**: un cliente que llame directamente a la API puede omitirlo.
No se habilita reCAPTCHA ni registro de actividad de Identity Platform sin
evaluar antes el costo y la posible retención de datos.

## Estado del piloto al 2026-10-14

- IAP del servicio piloto usa Identity Platform externo; una solicitud
  anónima recibe 302 al formulario propio. El backend piloto tiene cero
  bindings públicos; el servicio principal no recibió cambios.
- El formulario separado responde `/`, `/config` y `/bundle.js`; no sirve
  rutas de V0. La primera compilación corrigió su política CSP para permitir
  la llamada de configuración de Identity Platform.
- La verificación del flujo real detectó dos destinos que faltaban en la
  autorización del navegador: `iap.googleapis.com` como retorno de IAP en
  Identity Platform y el origen exacto del backend piloto en `connect-src`
  para que `gcip-iap` coloque su cookie. Se agregaron sin retirar los dominios
  existentes ni ampliar la política a otros destinos.
- La prueba de navegador integrada en Codex no llega a
  `www.googleapis.com` (`ERR_BLOCKED_BY_CLIENT`). Esto **no acredita ni
  descarta** el funcionamiento en Chrome normal. La persona titular completó
  fuera de esta conversación la rotación de contraseña y confirmó que el
  acceso válido en Chrome llega a «Resumen nacional»; la contraseña no se
  copia ni comunica aquí. La primera prueba manual de inactividad **falló**:
  después de más de 300 s seguían visibles los resultados. El fragmento
  periódico de Streamlit no se considera suficiente como control de cierre.
  Una candidata añade un temporizador en el documento que oculta los
  resultados antes de navegar al cierre de IAP y comprueba también el retorno
  desde una pestaña en segundo plano. Sus pruebas automatizadas no sustituyen
  una nueva prueba manual de 300 s; la reapertura también sigue pendiente.
- El formulario piloto usa la revisión `enares-stage04-auth-pilot-00008-fes`
  (digest `sha256:b6af37ddc276c55510b00b545955fe8097b4ac4eb4eed283344e6fa4e490d38e`).
  Pasó por candidata al 0 %, pruebas locales de la política CSP y CI verde
  del commit `253484704270a0cd24cbebadf819c356b6bc0053` antes de recibir
  el 100 % del tráfico **solo del servicio de acceso piloto**. La revisión
  anterior `00006-niq` conserva una URL etiquetada para rollback. El servicio
  principal `enares-stage04-shadow` no cambió.
- **Estado de publicación: NO PROMOVER.** Este PR continúa en borrador hasta
  comprobar todos los criterios siguientes y recibir la revisión de Rita.

El paquete de aceptación exige: acceso correcto e incorrecto, usuario
incorrecto, anónimo sin cifras, backend directo rechazado, IAM privado,
ausencia de lectura V0 preautenticación, bloqueo y nueva contraseña tras
300 s, controles antiabuso, secretos ausentes de artefactos, navegación de
seis módulos/80 temas, CI verde, digest/revisión de la candidata, rollback y
capacidad/costo registrados. El PR permanece en borrador hasta completar el
piloto y enviar **una sola** solicitud de revisión a Rita.

Referencias oficiales: [identidades externas de IAP](https://docs.cloud.google.com/iap/docs/enable-external-identities),
[cabeceras firmadas](https://docs.cloud.google.com/iap/docs/signed-headers-howto),
[sesiones externas](https://docs.cloud.google.com/iap/docs/external-identity-sessions).
