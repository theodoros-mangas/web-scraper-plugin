from __future__ import annotations

from collections import deque
from dataclasses import dataclass

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

        while queue and stats.pages_fetched < self.max_pages:
            url = queue.popleft()
            ctx = ParseContext(url=url)

            try:
                self.limiter.wait()
                res = self.fetcher.fetch(url)
                stats.pages_fetched += 1

                items = plugin.parse(ctx, res.text)
                cleaned = []
                for it in items:
                    it = normalize_item(it)
                    it = validate_item(it)
                    cleaned.append(it)

                if cleaned:
                    self.store.write_many(cleaned)
                    stats.items_saved += len(cleaned)

                for nxt in plugin.next_urls(ctx, res.text):
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append(nxt)

            except Exception:
                stats.errors += 1
                continue

        self.store.close()
        return stats
