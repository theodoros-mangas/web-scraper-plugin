from __future__ import annotations

from scraper.core.types import Item


def normalize_item(item: Item) -> Item:
    # Example: trim strings
    for k, v in list(item.items()):
        if isinstance(v, str):
            item[k] = v.strip()
    return item
