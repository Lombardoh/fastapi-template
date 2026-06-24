from __future__ import annotations

from enum import StrEnum


class ProductCondition(StrEnum):
    NEW = "new"
    USED = "used"
    REFURBISHED = "refurbished"
    OPEN_BOX = "open_box"
