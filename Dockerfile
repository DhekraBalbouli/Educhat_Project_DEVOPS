FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /opt/venv/bin/python -m spacy download en_core_web_sm



FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000 \
    HOST=0.0.0.0 \
    DB_PATH=/app/data/db.sqlite3

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        gcc \
        build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && node --version \
    && gcc --version

    COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY main.py mon_chatbot.py ./
COPY chatbot/ ./chatbot/
COPY api/     ./api/
COPY static/  ./static/
COPY corpus/  ./corpus/

RUN addgroup --system educhat && \
    adduser  --system --ingroup educhat educhat && \
    mkdir -p /app/data && \
    chown -R educhat:educhat /app

USER educhat

VOLUME ["/app/data"]

# Port d'écoute
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/langages')" \
    || exit 1

CMD ["uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--log-level", "info"]