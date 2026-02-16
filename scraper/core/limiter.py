from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class RateLimiter:
    """Simple global rate limiter (requests per second)."""
    rps: float = 2.0

    def __post_init__(self) -> None:
        self._min_interval = 1.0 / self.rps if self.rps > 0 else 0.0
        self._last = 0.0

    def wait(self) -> None:
        if self._min_interval <= 0:
            return
        now = time.perf_counter()
        elapsed = now - self._last
        sleep_for = self._min_interval - elapsed
        if sleep_for > 0:
            time.sleep(sleep_for)
        self._last = time.perf_counter()
