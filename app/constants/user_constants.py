from __future__ import annotations

from enum import StrEnum


class UserScope(StrEnum):
    USER = "user"
    ADMIN = "admin"
    B2B = "b2b"
