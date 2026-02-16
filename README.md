# web-scraper-plugin
A scraper framework where each site is a plugin
# plugin-web-scraper

A small but production-style scraping framework demonstrating clean architecture, extensibility, and testability in Python.

> This project is intentionally designed as an engineering showcase rather than a one-off script.

Instead of writing a new scraper for every website, the framework separates responsibilities:

* HTTP fetching & retry logic
* rate limiting
* parsing (site-specific plugins)
* data validation & normalization
* storage backend (JSONL or SQLite)
* CLI interface
* unit-testable core

The result: adding a new website requires only a single class.

---

## Architecture

```
                ┌──────────────┐
                │   Runner     │
                └──────┬───────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   Fetcher        RateLimiter      Store
        │                              │
        │                              │
        ▼                              ▼
              Scraper Plugin (per-site)
                     │
                     ▼
           Pipeline (validate + normalize)
```

### Design goals

* SOLID-style separation of concerns
* deterministic tests (no network dependency)
* reusable components
* minimal dependencies
* CLI-friendly UX

---

## Quickstart

Clone and run in under a minute:

```bash
git clone <repo-url>
cd plugin-web-scraper

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

List available plugins:

```bash
scrape list
```

Run the demo scraper:

```bash
scrape run quotes --max-pages 2
```

Output will appear in:

```
out/items.jsonl
```

---

## SQLite Storage

You can also store structured results in a database:

```bash
scrape run quotes --store sqlite --out out/quotes.db
```

Quick check:

```python
import sqlite3
conn = sqlite3.connect("out/quotes.db")
print(conn.execute("SELECT COUNT(*) FROM items").fetchone())
```

---

## Writing a New Plugin

Create one class only.

```python
from scraper.plugins.base import ScraperPlugin, ParseContext
from selectolax.parser import HTMLParser

class MySite(ScraperPlugin):
    name = "mysite"

    def start_urls(self):
        return ["https://example.com"]

    def parse(self, ctx: ParseContext, html: str):
        tree = HTMLParser(html)
        return [{
            "source": self.name,
            "url": ctx.url,
            "title": tree.css_first("h1").text(strip=True)
        }]
```

Register it in:

```
scraper/plugins/__init__.py
```

Run:

```
scrape run mysite
```

No other code changes required.

---

## Testing

All core logic is testable without internet access.

```
pytest -q
```

Tests cover:

* plugin registry
* retry policy
* runner orchestration
* storage backends

---

## Why this project exists

Many scraping examples online are tightly coupled scripts:

```
requests → parse → print → done
```

Real systems need:

* retries
* rate limiting
* storage abstraction
* extensibility
* deterministic tests

This repository demonstrates how to structure such a system cleanly in Python.

---

## Tradeoffs

| Decision         | Reason                     |
| ---------------- | -------------------------- |
| Sync first       | easier testing & reasoning |
| JSONL default    | reproducible outputs       |
| SQLite optional  | structured querying        |
| selectolax       | fast & lightweight parser  |
| explicit plugins | avoids implicit magic      |

Async support could be added without changing plugin interfaces.

---

## License

MIT
