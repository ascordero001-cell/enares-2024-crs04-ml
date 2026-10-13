# Acceso privado del piloto Stage 04

El requisito final solicitado por Ana es un formulario de usuario y contraseña
sin inicio de sesión con Google. En `STAGE04_DATA_MODE=AUTHENTICATED_SHADOW`,
la aplicación exige ese formulario **antes** de abrir el repositorio de
agregados V0. El modo local de desarrollo conserva el flujo anterior.

Esta implementación es todavía una candidata de código, no una autorización
para quitar IAP ni para admitir tráfico público. El piloto y el servicio
principal conservan su protección actual hasta que la supervisión apruebe
expresamente una arquitectura de acceso sin Google, sus controles antiabuso,
sesiones y rollback. Una clave compartida no proporciona identidad ni
revocación individual; la contraseña comunicada anteriormente debe rotarse
antes de un despliegue expuesto a Internet.

El despliegue configuraría `STAGE04_LOGIN_USERNAME=vigilancia` y
`STAGE04_LOGIN_PASSWORD_HASH` fuera del repositorio. El hash tiene formato
`pbkdf2_sha256$600000$<sal hexadecimal de al menos 16 bytes>$<digest hexadecimal
de 32 bytes>`. La contraseña en claro nunca se incluye en Git, Docker, logs,
URLs ni comentarios de GitHub. Para generar un hash nuevo, usar un entorno
privado y una lectura interactiva sin eco; no pasar la contraseña como argumento
de línea de comandos. Si falta la configuración o el hash es inválido, el
servicio no muestra cifras.

Cada nueva sesión de Streamlit presenta el formulario. Tras 300 segundos sin interacción con la aplicación,
se borran el estado local, los filtros y los resultados; para continuar se
vuelve a introducir el usuario y la contraseña. En el piloto actual, IAP tiene
una política independiente de reautenticación `LOGIN` con `maxAge=300s`; ese
piloto **todavía muestra Google** y no satisface el requisito final.

Antes de cualquier piloto sin Google: decisión de arquitectura supervisora,
contraseña nueva y fuerte, configuración fuera de Git, protección contra
intentos automatizados, revisión independiente del PR y su CI, prueba manual
del formulario con credenciales válidas e inválidas, expiración a 300 segundos,
comprobación de que el anónimo no ve cifras, candidata aislada y rollback
disponible. No reutilizar la contraseña compartida actual como único control.
