from __future__ import annotations

from scraper.core.types import Item


def normalize_item(item: Item) -> Item:
    normalized = dict(item)
    for k, v in list(normalized.items()):
        if isinstance(v, str):
            normalized[k] = v.strip()
    return normalized
