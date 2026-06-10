from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from app.api.routes import health
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(health.router)


def main() -> None:
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)


if __name__ == "__main__":
    main()
