# plugin-web-scraper

A small Python project that treats scraping as a maintainable system instead of a disposable script.

The codebase is intentionally compact, but the boundaries are real: fetching, retry policy, rate limiting, parsing, validation, storage, and CLI execution are all isolated and testable. That makes it useful both as a learning project and as a portfolio example.

## What it demonstrates

- A plugin registry for site-specific scraping logic
- A reusable runner that orchestrates fetch, parse, validate, and persist steps
- A deterministic test suite that does not need live network access
- A CLI that is simple to use and easy to extend
- A deliberately sync-first design that favors clarity over premature complexity

## Project layout

```text
scraper/
├── cli.py              # Typer entrypoint
├── config.py           # Runtime configuration and validation
├── core/
│   ├── fetcher.py      # HTTP fetching + retry integration
│   ├── limiter.py      # Global rate limiting
│   ├── retry.py        # Exponential backoff policy
│   ├── runner.py       # Main orchestration loop
│   └── types.py        # Shared runtime types
├── pipeline/
│   ├── transforms.py   # Normalization
│   └── validators.py   # Schema-ish validation
├── plugins/
│   ├── base.py         # Plugin contract
│   ├── quotes.py       # Example scraper plugin
│   └── registry.py     # Explicit plugin registration
└── storage/
    ├── base.py         # Storage interface
    └── jsonl.py        # JSONL implementation
```

## Quick start

```bash
git clone https://github.com/theodoros-mangas/web-scraper-plugin.git
cd web-scraper-plugin

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
```

List the available plugins:

```bash
scrape list
```

Run the demo scraper against quotes.toscrape.com:

```bash
scrape run quotes --max-pages 2 --out out/items.jsonl
```

The command prints a short run summary and appends normalized records to out/items.jsonl.

## How a plugin fits in

Each plugin owns only site-specific behavior:

- where to start
- how to parse a page
- how to discover the next page

Everything else stays in the framework.

```python
from selectolax.parser import HTMLParser

from scraper.core.types import Item
from scraper.plugins.base import ParseContext, ScraperPlugin


class MySitePlugin(ScraperPlugin):
    name = "mysite"

    def start_urls(self) -> list[str]:
        return ["https://example.com"]

    def parse(self, ctx: ParseContext, html: str) -> list[Item]:
        tree = HTMLParser(html)
        heading = tree.css_first("h1")
        if not heading:
            return []

        return [
            {
                "source": self.name,
                "url": ctx.url,
                "title": heading.text(strip=True),
            }
        ]
```

Register the class in scraper/plugins/__init__.py and it becomes available through the CLI.

## Design choices

| Decision | Why it exists |
| --- | --- |
| Sync-first execution | Easier to reason about, easier to test, enough for a showcase-sized framework |
| Explicit plugin registry | No hidden imports or auto-discovery magic |
| JSONL output | Simple, diffable, and easy to inspect locally |
| Validation after parsing | Keeps plugin code focused on extraction |
| Small public surface area | Lower maintenance cost and cleaner extension points |

## Testing

The tests cover the parts recruiters usually look for when they open a small Python repo:

- registry behavior and failure cases
- retry timing behavior
- runner orchestration, cleanup, and error handling

Run them with:

```bash
pytest
```

## Current limitations

This is still a small framework, not a full crawler. A few obvious next steps would be:

- richer item schemas per plugin
- structured logging
- multiple storage backends
- async fetching for high-throughput workloads

Those are intentionally left out so the current design stays readable.

## License

MIT
