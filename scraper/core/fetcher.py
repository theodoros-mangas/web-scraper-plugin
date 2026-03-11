from __future__ import annotations

import httpx
from dataclasses import dataclass, field

from .exceptions import FetchError
from .retry import RetryPolicy
from .types import FetchResult


@dataclass(slots=True)
class Fetcher:
    timeout_s: float = 15.0
    user_agent: str = "plugin-web-scraper/0.1.0"
    retry: RetryPolicy = field(default_factory=RetryPolicy)

    def fetch(self, url: str) -> FetchResult:
        headers = {"User-Agent": self.user_agent}

        last_exc: httpx.HTTPError | None = None
        for attempt in range(1, self.retry.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout_s, headers=headers, follow_redirects=True) as client:
                    resp = client.get(url)
                resp.raise_for_status()
                return FetchResult(
                    url=url,
                    status_code=resp.status_code,
                    text=resp.text,
                    headers=dict(resp.headers),
                )
            except httpx.HTTPError as exc:
                last_exc = exc
                if attempt < self.retry.max_retries:
                    self.retry.sleep_before_retry(attempt)
                else:
                    break

        raise FetchError(f"Failed to fetch {url}: {last_exc}")
