from __future__ import annotations

import random
import time
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_retries: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 6.0
    jitter_factor: float = 0.2

    def __post_init__(self) -> None:
        if self.max_retries < 1:
            raise ValueError("max_retries must be at least 1")
        if self.base_delay_seconds < 0:
            raise ValueError("base_delay_seconds cannot be negative")
        if self.max_delay_seconds < self.base_delay_seconds:
            raise ValueError("max_delay_seconds must be >= base_delay_seconds")
        if self.jitter_factor < 0:
            raise ValueError("jitter_factor cannot be negative")

    def backoff_delay(self, attempt: int) -> float:
        if attempt < 1:
            raise ValueError("attempt must be at least 1")

        raw_delay = min(
            self.max_delay_seconds,
            self.base_delay_seconds * (2 ** (attempt - 1)),
        )
        jitter_multiplier = 1.0 + random.uniform(-self.jitter_factor, self.jitter_factor)
        return max(0.0, raw_delay * jitter_multiplier)

    def sleep_before_retry(self, attempt: int) -> None:
        """Sleep before the next retry using exponential backoff with jitter."""
        time.sleep(self.backoff_delay(attempt))