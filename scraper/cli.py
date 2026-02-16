from __future__ import annotations

from pathlib import Path

import typer

from scraper.config import ScrapeConfig
from scraper.core.fetcher import Fetcher
from scraper.core.limiter import RateLimiter
from scraper.core.runner import Runner
from scraper.plugins import build_registry
from scraper.storage.jsonl import JSONLStore
from scraper.utils.logging import console

app = typer.Typer(add_completion=False)


@app.command("list")
def list_plugins():
    reg = build_registry()
    console.print("[bold]Available plugins:[/bold]")
    for name in reg.list_names():
        console.print(f" - {name}")


@app.command("run")
def run(
    plugin: str = typer.Argument(..., help="Plugin name (e.g. quotes)"),
    max_pages: int = typer.Option(10, help="Max pages to fetch"),
    rps: float = typer.Option(2.0, help="Requests per second"),
    timeout_s: float = typer.Option(15.0, help="Request timeout seconds"),
    out: str = typer.Option("out/items.jsonl", help="Output JSONL path"),
):
    cfg = ScrapeConfig(plugin=plugin, max_pages=max_pages, rps=rps, timeout_s=timeout_s, out=out)

    reg = build_registry()
    plg = reg.create(cfg.plugin)

    fetcher = Fetcher(timeout_s=cfg.timeout_s, user_agent=cfg.user_agent)
    limiter = RateLimiter(rps=cfg.rps)
    store = JSONLStore(Path(cfg.out))

    runner = Runner(fetcher=fetcher, limiter=limiter, store=store, max_pages=cfg.max_pages)
    stats = runner.run(plg)

    console.print("\n[bold green]Done[/bold green]")
    console.print(f"Pages fetched: {stats.pages_fetched}")
    console.print(f"Items saved:   {stats.items_saved}")
    console.print(f"Errors:        {stats.errors}")
    console.print(f"Output:        {cfg.out}")
