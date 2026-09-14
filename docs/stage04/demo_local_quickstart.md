# Quickstart reproducible — Stage 04 local shadow

**Alcance:** `LOCAL_SHADOW_ONLY`

**Cloud:** `NOT_AUTHORIZED`

**Verificación independiente desde clon limpio:** `PENDING`

Este procedimiento levanta únicamente la aplicación local con agregados V0 autorizados y el
fixture sintético versionado. No ejecuta `gcloud`, no crea recursos y no publica resultados.

## Opción A — Python 3.12 en Windows PowerShell

```powershell
git clone https://github.com/ascordero001-cell/enares-2024-crs04-ml.git
cd enares-2024-crs04-ml
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest tests/test_naming.py -q
python -m pytest -q
python scripts/release_diagnostic.py --expected-release enares2024-crs04-v0-shadow-001
python -m streamlit run app/streamlit_app.py
```

La aplicación debe abrir en `http://localhost:8501`. El diagnóstico debe devolver JSON con
`"status": "ok"`, los módulos 3.1–3.6 y `"cloud": "NOT_AUTHORIZED"`.

## Opción B — contenedor local

Requiere un motor Docker en ejecución:

```powershell
docker build --tag enares-stage04:local .
docker run --detach --name enares-stage04 --publish 8080:8080 enares-stage04:local
docker inspect --format='{{.State.Health.Status}}' enares-stage04
curl.exe --fail http://127.0.0.1:8080/_stcore/health
docker exec enares-stage04 python scripts/release_diagnostic.py --expected-release enares2024-crs04-v0-shadow-001
docker rm --force enares-stage04
```

Resultados esperados:

- la imagen construye sin credenciales ni archivos privados;
- el contenedor queda `healthy` y la aplicación responde en `http://localhost:8080`;
- el health responde `ok`;
- el diagnóstico devuelve `status=ok` para el release esperado;
- la imagen contiene `streamlit==1.63.0`;
- el estado cloud continúa `NOT_AUTHORIZED`.

## Registro de verificación independiente

La persona verificadora debe ejecutar desde un clon nuevo y registrar en el PR:

- nombre o usuario GitHub;
- sistema operativo y versión de Python o Docker;
- SHA verificado;
- resultado de instalación/build;
- resultado de `pytest`;
- salida del diagnóstico de release;
- URL local comprobada y resultado del health;
- fecha UTC.

No se marca esta verificación como completada hasta recibir esa evidencia de una persona distinta
de la autora. Fallos de instalación, health o release bloquean el cierre del paso 36, pero no
autorizan cambios cloud.
