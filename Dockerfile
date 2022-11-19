# Separate build image
FROM python:3.10-slim-buster as compile-image
RUN python -m venv /opt/venv2
ENV PATH="/opt/venv2/bin:$PATH"
ENV BOT_NAME=$BOT_NAME
COPY requirements.txt .

RUN apt-get update \
 && apt-get -y install libpq-dev libpq5 gcc \
 && pip install --no-cache-dir psycopg2-binary \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*

# Final image
FROM python:3.10-slim-buster
COPY --from=compile-image /opt/venv2 /opt/venv2
RUN apt-get update && apt-get install libpq5 -y
ENV PATH="/opt/venv2/bin:$PATH"
ENV BOT_NAME=$BOT_NAME
WORKDIR /app
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY bot /app/bot
COPY .env /app
CMD ["python", "-m", "bot"]
