from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

Item = Dict[str, Any]

@dataclass(frozen=True)
class FetchResult:
    url: str
    status_code: int
    text: str
    headers: Dict[str, str]