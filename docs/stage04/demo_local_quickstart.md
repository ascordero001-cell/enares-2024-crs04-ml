# Quickstart reproducible — Stage 04 local shadow

**Alcance:** `LOCAL_SHADOW_ONLY`

**Cloud:** `NOT_AUTHORIZED`

**Verificación en runner limpio:** `AUTOMATED_BY_QUICKSTART_CI`

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

## Validación automatizada en runner limpio

El job `Clean-runner quickstart` extrae y ejecuta directamente el siguiente bloque. El workflow no
mantiene una copia de estos comandos, por lo que una desincronización entre la guía y el repositorio
hace fallar el PR.

```bash quickstart-ci
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -c "import streamlit; assert streamlit.__version__ == '1.63.0'"
python -m pytest tests/test_naming.py -q
python -m pytest -q
python scripts/release_diagnostic.py --expected-release enares2024-crs04-v0-shadow-001
python -m streamlit run app/streamlit_app.py --server.headless=true --server.address=127.0.0.1 --server.port=8501 > /tmp/enares-quickstart.log 2>&1 &
app_pid=$!
trap 'kill "$app_pid" 2>/dev/null || true' EXIT
for attempt in $(seq 1 30); do
  if curl --fail --silent http://127.0.0.1:8501/_stcore/health | grep --quiet '^ok$'; then
    break
  fi
  if [ "$attempt" -eq 30 ]; then
    cat /tmp/enares-quickstart.log
    exit 1
  fi
  sleep 1
done
curl --fail --silent --show-error http://127.0.0.1:8501/ > /dev/null
```

El control se ejecuta en un checkout nuevo, sin credenciales ni cuenta de Google, y cubre
instalación, pruebas, versión fijada de Streamlit, diagnóstico del release, arranque y health. El
riesgo residual es que comprueba comandos ejecutables, pero no que una persona lea o comprenda la
prosa de esta guía. Un fallo bloquea el paso 36 y no autoriza cambios cloud.
