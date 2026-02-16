from __future__ import annotations

import random
import time
from dataclasses import dataclass

@dataclass(frozen=True)
class RetryPolicy:
    max_retries: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 6.0
    jitter_factor: float = 0.2
    
    def sleep_before_retry(self, attempt: int) -> None:
        """Exponential backoff with jitter. attempt starts at 1 for first retry."""
        raw = min(self.max_delay_seconds, self.base_delay_seconds * (2 ** (attempt - 1)))
        jitter_factor = 1.0 + random.uniform(-self.jitter_factor, self.jitter_factor)
        time.sleep(max(0.0, raw * jitter_factor))