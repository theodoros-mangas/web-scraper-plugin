from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from scraper.core.types import Item


@dataclass(frozen=True)
class ParseContext:
    url: str


class ScraperPlugin(ABC):
    """Per-site plugin. Implement only site-specific logic here."""

    name: str

    @abstractmethod
    def start_urls(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def parse(self, ctx: ParseContext, html: str) -> list[Item]:
        raise NotImplementedError

    def next_urls(self, ctx: ParseContext, html: str) -> Iterable[str]:
        return []
