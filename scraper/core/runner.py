from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from scraper.core.fetcher import Fetcher
from scraper.core.limiter import RateLimiter
from scraper.plugins.base import ParseContext, ScraperPlugin
from scraper.pipeline.transforms import normalize_item
from scraper.pipeline.validators import validate_item
from scraper.storage.base import Store


@dataclass
class RunStats:
    pages_fetched: int = 0
    items_saved: int = 0
    errors: int = 0
    failed_urls: list[str] = field(default_factory=list)


@dataclass
class Runner:
    fetcher: Fetcher
    limiter: RateLimiter
    store: Store
    max_pages: int = 50

    def run(self, plugin: ScraperPlugin) -> RunStats:
        stats = RunStats()
        queue = deque(plugin.start_urls())
        seen: set[str] = set(queue)

        try:
            while queue and stats.pages_fetched < self.max_pages:
                url = queue.popleft()
                ctx = ParseContext(url=url)

                try:
                    self.limiter.wait()
                    res = self.fetcher.fetch(url)
                    stats.pages_fetched += 1

                    cleaned = self._clean_items(plugin.parse(ctx, res.text))
                    if cleaned:
                        self.store.write_many(cleaned)
                        stats.items_saved += len(cleaned)

                    for next_url in plugin.next_urls(ctx, res.text):
                        if next_url and next_url not in seen:
                            seen.add(next_url)
                            queue.append(next_url)

                except Exception:
                    stats.errors += 1
                    stats.failed_urls.append(url)
        finally:
            self.store.close()

        return stats

    @staticmethod
    def _clean_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
        cleaned: list[dict[str, object]] = []
        for item in items:
            normalized = normalize_item(item)
            cleaned.append(validate_item(normalized))
        return cleaned
