from __future__ import annotations

from dataclasses import dataclass

from scraper.core.fetcher import Fetcher
from scraper.core.limiter import RateLimiter
from scraper.core.runner import Runner
from scraper.core.types import FetchResult
from scraper.plugins.base import ParseContext, ScraperPlugin
from scraper.storage.base import Store

HTML = """
<html>
  <div class="quote">
    <span class="text">"Hello"</span>
    <small class="author">Me</small>
    <div class="tags"><a class="tag">test</a></div>
  </div>
</html>
"""


class DummyPlugin(ScraperPlugin):
    name = "dummy"

    def start_urls(self) -> list[str]:
        return ["http://example.test/"]

    def parse(self, ctx: ParseContext, html: str):
        return [{"source": "dummy", "url": f"  {ctx.url}  ", "value": " ok "}]


class FailingPlugin(ScraperPlugin):
    name = "failing"

    def start_urls(self) -> list[str]:
        return ["http://example.test/boom", "http://example.test/ok"]

    def parse(self, ctx: ParseContext, html: str):
        if ctx.url.endswith("boom"):
            raise ValueError("broken parser")
        return [{"source": "failing", "url": ctx.url, "value": "ok"}]


@dataclass
class MemoryStore(Store):
    items: list[dict]
    closed: bool = False

    def write_many(self, items) -> None:
        self.items.extend(items)

    def close(self) -> None:
        self.closed = True


class FakeFetcher(Fetcher):
    def fetch(self, url: str) -> FetchResult:
        return FetchResult(url=url, status_code=200, text=HTML, headers={})


def test_runner_saves_items():
    store = MemoryStore(items=[])
    runner = Runner(fetcher=FakeFetcher(), limiter=RateLimiter(rps=0), store=store, max_pages=1)
    stats = runner.run(DummyPlugin())

    assert stats.pages_fetched == 1
    assert stats.items_saved == 1
    assert store.items == [{"source": "dummy", "url": "http://example.test/", "value": "ok"}]
    assert store.closed is True


def test_runner_records_failures_and_continues():
    store = MemoryStore(items=[])
    runner = Runner(fetcher=FakeFetcher(), limiter=RateLimiter(rps=0), store=store, max_pages=2)

    stats = runner.run(FailingPlugin())

    assert stats.pages_fetched == 2
    assert stats.items_saved == 1
    assert stats.errors == 1
    assert stats.failed_urls == ["http://example.test/boom"]
    assert store.closed is True
