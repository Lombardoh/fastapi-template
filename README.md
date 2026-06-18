# Checkpoint

FastAPI service base using Poetry, Pydantic settings, SQLAlchemy async, PostgreSQL, and Alembic.

The application uses a top-level `app` package, with FastAPI routes separated from
configuration, database setup, models, schemas, and services.

```text
app/
  api/
    routes/
  core/
  db/
  models/
  schemas/
  services/
```

## Setup

```powershell
poetry env use (py -3.14 -c "import sys; print(sys.executable)")
poetry install
Copy-Item .env.example .env
docker compose up -d postgres
```

Configuration is read from environment variables or a local `.env` file. The expected keys are listed in `.env.example`.
The local database uses PostgreSQL 18 so model primary keys can use native `uuidv7()`.
The application runs on the host, so `DATABASE_URL` must use the exposed host port, `5436`.

## Alembic

```powershell
poetry run alembic upgrade head
```

## Pre-commit

```powershell
poetry run pre-commit install
poetry run pre-commit run --all-files
```

## Run

```powershell
poetry run uvicorn app.main:app --reload
```
