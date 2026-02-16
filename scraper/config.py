from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScrapeConfig:
    plugin: str
    max_pages: int = 10
    rps: float = 2.0
    timeout_s: float = 15.0
    user_agent: str = "plugin-web-scraper/0.1.0"
    out: str = "out/items.jsonl"
