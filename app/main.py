from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from app.api.routes import auth, health
from app.core.config import settings
from app.exceptions import ApplicationError
from app.exceptions.handlers import application_error_handler

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.add_exception_handler(ApplicationError, application_error_handler)
app.include_router(auth.router)
app.include_router(health.router)


def main() -> None:
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)


if __name__ == "__main__":
    main()
