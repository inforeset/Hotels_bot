# Separate build image
FROM python:3.10-slim-buster as builder


RUN apt-get update \
 && apt-get -y install libpq-dev libpq5 gcc \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir psycopg2-binary \
 && pip install --no-cache-dir setuptools wheel \
 && rm -rf /var/lib/apt/lists/*

# Final image
FROM builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini /app/alembic.ini

COPY alembic /app/alembic

COPY bot /app/bot

CMD ["python", "-m", "bot"]
