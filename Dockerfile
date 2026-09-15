FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY requirements-runtime.txt ./requirements-runtime.txt

RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements-runtime.txt \
    && addgroup --system app \
    && adduser --system --ingroup app app

COPY --chown=app:app app ./app
COPY --chown=app:app src ./src
COPY --chown=app:app scripts/container_healthcheck.py scripts/release_diagnostic.py ./scripts/
COPY --chown=app:app docs/stage04/v0_drive_hash_manifest.md ./docs/stage04/v0_drive_hash_manifest.md

USER app

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 \
    CMD ["python", "scripts/container_healthcheck.py"]

CMD ["sh", "-c", "exec python -m streamlit run app/streamlit_app.py --server.address=0.0.0.0 --server.port=${PORT:-8080} --server.headless=true --browser.gatherUsageStats=false"]
