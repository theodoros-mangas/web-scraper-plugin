from __future__ import annotations

from selectolax.parser import HTMLParser

from scraper.core.types import Item
from scraper.plugins.base import ParseContext, ScraperPlugin


class QuotesToScrapePlugin(ScraperPlugin):
    name = "quotes"

    def start_urls(self) -> list[str]:
        return ["https://quotes.toscrape.com/"]

    def parse(self, ctx: ParseContext, html: str) -> list[Item]:
        tree = HTMLParser(html)
        items: list[Item] = []

        for q in tree.css("div.quote"):
            text = q.css_first("span.text")
            author = q.css_first("small.author")
            tags = [t.text(strip=True) for t in q.css("div.tags a.tag")]

            if not text or not author:
                continue

            items.append(
                {
                    "source": self.name,
                    "url": ctx.url,
                    "quote": text.text(strip=True),
                    "author": author.text(strip=True),
                    "tags": tags,
                }
            )

        return items

    def next_urls(self, ctx: ParseContext, html: str):
        tree = HTMLParser(html)
        next_a = tree.css_first("li.next a")
        if next_a:
            href = next_a.attributes.get("href")
            # site uses relative links
            if href and href.startswith("http"):
                yield href
            elif href:
                yield "https://quotes.toscrape.com" + href
