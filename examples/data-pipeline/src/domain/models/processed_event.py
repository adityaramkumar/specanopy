# generated_from: contracts/schemas/processed
# spec_hash: 363cd030c1920e3fa5120a35d07ebe130a62a4e292bbc5d4b4f784afb869fbf9
# generated_at: 2026-03-10T09:07:01.356779+00:00
# agent: implementation-agent

from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class ProcessedEvent:
    event_id: str
    event_type: str
    timestamp_utc: str
    date: str
    hour: int
    user_id: str
    is_anonymous: bool
    source: str
    properties: Dict[str, Any]
    enrichments: Dict[str, Any]