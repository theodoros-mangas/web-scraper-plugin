from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from scraper.core.types import Item
from scraper.storage.base import Store


@dataclass
class JSONLStore(Store):
    path: Path

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

    def write_many(self, items: list[Item]) -> None:
        for item in items:
            self._fh.write(json.dumps(item, ensure_ascii=False) + "\n")
        self._fh.flush()

    def close(self) -> None:
        try:
            self._fh.close()
        except Exception:
            pass
