from __future__ import annotations

import httpx
from dataclasses import dataclass

from .exceptions import FetchError
from .retry import RetryPolicy
from .types import FetchResult


@dataclass
class Fetcher:
    timeout_s: float = 15.0
    user_agent: str = "plugin-web-scraper/0.1.0"
    retry: RetryPolicy = RetryPolicy()

    def fetch(self, url: str) -> FetchResult:
        headers = {"User-Agent": self.user_agent}

        last_exc: Exception | None = None
        for attempt in range(1, self.retry.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout_s, headers=headers, follow_redirects=True) as client:
                    resp = client.get(url)
                return FetchResult(
                    url=url,
                    status_code=resp.status_code,
                    text=resp.text,
                    headers=dict(resp.headers),
                )
            except Exception as exc:
                last_exc = exc
                if attempt < self.retry.max_retries:
                    self.retry.sleep_before_retry(attempt)
                else:
                    break

        raise FetchError(f"Failed to fetch {url}: {last_exc}")
