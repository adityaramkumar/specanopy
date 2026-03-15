# generated_from: behaviors/transform
# spec_hash: b23f1b9a2a7857231ad8294350b7954c38e2dfeb90460a03b6e6ac8603bea4ac
# generated_at: 2026-03-15T02:32:31.307691+00:00
# agent: implementation-agent
from datetime import datetime, timezone
from .events import RawEvent, ProcessedEvent


def process_event(raw: RawEvent) -> ProcessedEvent:
    """
    Transform single raw event to processed event.

    - Convert timestamp to UTC
    - Derive date (YYYY-MM-DD) and hour (0-23)
    - Handle anonymous user_id

    Args:
        raw: Validated RawEvent

    Returns:
        ProcessedEvent
    """
    # Parse timestamp and convert to UTC
    dt = datetime.fromisoformat(raw.timestamp.replace('Z', '+00:00'))
    timestamp_utc = dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

    # Derive date and hour
    date = dt.astimezone(timezone.utc).strftime('%Y-%m-%d')
    hour = dt.astimezone(timezone.utc).hour

    # Handle user_id
    user_id = raw.user_id or 'anonymous'
    is_anonymous = raw.user_id is None

    return ProcessedEvent(
        event_id=str(raw.event_id),
        event_type=raw.event_type,
        timestamp_utc=timestamp_utc,
        date=date,
        hour=hour,
        user_id=user_id,
        is_anonymous=is_anonymous,
        source=raw.source,
        properties=raw.properties
    )


def compare_events_by_timestamp(a: ProcessedEvent, b: ProcessedEvent) -> int:
    """
    Comparator for sorting events by timestamp_utc ascending.

    Args:
        a: First ProcessedEvent
        b: Second ProcessedEvent

    Returns:
        Negative if a before b, zero if equal, positive if a after b
    """
    if a.timestamp_utc < b.timestamp_utc:
        return -1
    elif a.timestamp_utc > b.timestamp_utc:
        return 1
    else:
        return 0
