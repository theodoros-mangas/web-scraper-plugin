from __future__ import annotations

from scraper.core.types import Item


def validate_item(item: Item) -> Item:
    required = ["source", "url"]
    for key in required:
        if key not in item or not item[key]:
            raise ValueError(f"Missing required field: {key}")
    return item
