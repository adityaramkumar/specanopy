# generated_from: contracts/schemas/processed
# spec_hash: 363cd030c1920e3fa5120a35d07ebe130a62a4e292bbc5d4b4f784afb869fbf9
# generated_at: 2026-03-10T09:07:01.356779+00:00
# agent: implementation-agent

from abc import ABC, abstractmethod
from typing import List
from domain.models.processed_event import ProcessedEvent

class EventRepository(ABC):
    @abstractmethod
    def save_batch(self, events: List[ProcessedEvent]):
        pass