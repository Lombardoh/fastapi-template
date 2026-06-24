from __future__ import annotations

import json
from pathlib import Path

from fastapi import Request
from fastapi.responses import JSONResponse

from app.constants.config_constants import AVAILABLE_LOCALES, DEFAULT_LOCALE
from app.exceptions.base import ApplicationError

LOCALES_PATH = Path(__file__).resolve().parent.parent / "locales"
TRANSLATIONS = {
    locale: json.loads((LOCALES_PATH / f"{locale}.json").read_text(encoding="utf-8"))
    for locale in AVAILABLE_LOCALES
}


async def application_error_handler(
    _request: Request,
    exception: ApplicationError,
) -> JSONResponse:
    locale = exception.locale if exception.locale in AVAILABLE_LOCALES else DEFAULT_LOCALE
    message = (
        TRANSLATIONS[locale].get(exception.code)
        or TRANSLATIONS[DEFAULT_LOCALE].get(exception.code)
        or exception.code
    )
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "code": exception.code,
                "message": message,
            }
        },
    )
