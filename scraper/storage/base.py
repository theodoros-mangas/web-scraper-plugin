from __future__ import annotations

from abc import ABC, abstractmethod
from scraper.core.types import Item


class Store(ABC):
    @abstractmethod
    def write_many(self, items: list[Item]) -> None:
        raise NotImplementedError

    def close(self) -> None:
        return None
