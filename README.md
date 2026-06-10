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
poetry install
Copy-Item .env.example .env
```

Configuration is read from environment variables or a local `.env` file. The expected keys are listed in `.env.example`.

## Alembic

Initialize Alembic after installing dependencies:

```powershell
poetry run alembic init migrations
```

Then configure `migrations/env.py` to use the application settings and SQLAlchemy metadata:

```python
from app.core.config import settings
from app.db.base import Base
import app.models

config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata
```

After Alembic is configured:

```powershell
poetry run alembic revision --autogenerate -m "initial migration"
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
