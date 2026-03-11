from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScrapeConfig:
    plugin: str
    max_pages: int = 10
    rps: float = 2.0
    timeout_s: float = 15.0
    user_agent: str = "plugin-web-scraper/0.1.0"
    out: str = "out/items.jsonl"

    def __post_init__(self) -> None:
        if not self.plugin.strip():
            raise ValueError("plugin must be a non-empty string")
        if self.max_pages < 1:
            raise ValueError("max_pages must be at least 1")
        if self.rps < 0:
            raise ValueError("rps cannot be negative")
        if self.timeout_s <= 0:
            raise ValueError("timeout_s must be greater than 0")
        if not self.out.strip():
            raise ValueError("out must be a non-empty path")
