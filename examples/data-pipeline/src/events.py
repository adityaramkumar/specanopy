# generated_from: behaviors/transform
# spec_hash: b23f1b9a2a7857231ad8294350b7954c38e2dfeb90460a03b6e6ac8603bea4ac
# generated_at: 2026-03-15T02:32:31.306330+00:00
# agent: implementation-agent
from dataclasses import dataclass
from typing import Dict, Any, Optional
from uuid import UUID
import re


@dataclass
class RawEvent:
    event_id: UUID
    event_type: str
    timestamp: str
    user_id: Optional[str]
    properties: Dict[str, Any]
    source: str


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


def validate_raw_event(data: Dict[str, Any]) -> RawEvent:
    """
    Validate raw event data and return RawEvent or raise ValueError.

    Args:
        data: Raw JSON dict from NDJSON line

    Returns:
        Validated RawEvent

    Raises:
        ValueError: If validation fails
    """
    try:
        # Validate required fields exist
        if 'event_id' not in data:
            raise ValueError('missing event_id')
        if 'event_type' not in data:
            raise ValueError('missing event_type')
        if 'timestamp' not in data:
            raise ValueError('missing timestamp')
        if 'properties' not in data:
            raise ValueError('missing properties')
        if 'source' not in data:
            raise ValueError('missing source')

        # Validate event_id UUID
        try:
            event_id = UUID(data['event_id'])
        except ValueError:
            raise ValueError('invalid event_id UUID')

        # Validate event_type
        allowed_types = {'page_view', 'click', 'purchase', 'signup'}
        if data['event_type'] not in allowed_types:
            raise ValueError(f'invalid event_type: {data["event_type"]}')

        # Validate timestamp (basic ISO 8601 check)
        timestamp = data['timestamp']
        if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})$', timestamp):
            raise ValueError('invalid timestamp format')

        # Validate properties is dict
        if not isinstance(data['properties'], dict):
            raise ValueError('properties must be object')

        # Validate source
        allowed_sources = {'web', 'mobile', 'api'}
        if data['source'] not in allowed_sources:
            raise ValueError(f'invalid source: {data["source"]}')

        # user_id is optional
        user_id = data.get('user_id')

        return RawEvent(
            event_id=event_id,
            event_type=data['event_type'],
            timestamp=timestamp,
            user_id=user_id,
            properties=data['properties'],
            source=data['source']
        )
    except Exception as e:
        raise ValueError(f'event validation failed: {str(e)}')


def raw_event_to_processed(raw: RawEvent) -> ProcessedEvent:
    """
    Convert validated RawEvent to ProcessedEvent (called by processing functions).

    Args:
        raw: Validated RawEvent

    Returns:
        ProcessedEvent
    """
    from .processing import process_event
    return process_event(raw)
