from dataclasses import dataclass
from scraper.core.runner import Runner
from scraper.core.types import FetchResult
from scraper.plugins.base import ParseContext, ScraperPlugin
from scraper.storage.base import Store
from scraper.core.limiter import RateLimiter
from scraper.core.fetcher import Fetcher

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
    def start_urls(self): return ["http://example.test/"]
    def parse(self, ctx: ParseContext, html: str):
        return [{"source": "dummy", "url": ctx.url, "value": "ok"}]

@dataclass
class MemoryStore(Store):
    items: list[dict]
    def write_many(self, items): self.items.extend(items)

class FakeFetcher(Fetcher):
    def fetch(self, url: str) -> FetchResult:
        return FetchResult(url=url, status_code=200, text=HTML, headers={})

def test_runner_saves_items():
    runner = Runner(fetcher=FakeFetcher(), limiter=RateLimiter(rps=0), store=MemoryStore(items=[]), max_pages=1)
    stats = runner.run(DummyPlugin())
    assert stats.pages_fetched == 1
    assert stats.items_saved == 1
