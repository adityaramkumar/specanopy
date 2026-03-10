# generated_from: contracts/schemas/processed
# spec_hash: 363cd030c1920e3fa5120a35d07ebe130a62a4e292bbc5d4b4f784afb869fbf9
# generated_at: 2026-03-10T09:07:01.356779+00:00
# agent: implementation-agent

from datetime import datetime
from domain.models.processed_event import ProcessedEvent

class EventTransformer:
    def transform(self, raw_event: dict, session_id: str, sequence: int) -> ProcessedEvent:
        ts = datetime.fromisoformat(raw_event['timestamp_utc'].replace('Z', '+00:00'))
        user_id = raw_event.get('user_id') or 'anonymous'
        
        return ProcessedEvent(
            event_id=raw_event['event_id'],
            event_type=raw_event['event_type'],
            timestamp_utc=raw_event['timestamp_utc'],
            date=ts.strftime('%Y-%m-%d'),
            hour=ts.hour,
            user_id=user_id,
            is_anonymous=(user_id == 'anonymous'),
            source=raw_event['source'],
            properties=raw_event.get('properties', {}),
            enrichments={'session_id': session_id, 'event_sequence': sequence}
        )