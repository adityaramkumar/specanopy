# generated_from: behaviors/load
# spec_hash: 0b934202a49f4432570d0cc3738b0361a1088861a4ceeb405e5962435271ca4f
# generated_at: 2026-03-15T02:31:41.319543+00:00
# agent: implementation-agent
from typing import Any


def sort_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Sort events by timestamp_utc ascending.

    Args:
        events: List of processed events

    Returns:
        list[dict[str, Any]]: Events sorted by timestamp_utc

    Raises:
        ValueError: If any event missing 'timestamp_utc' or invalid ISO format
    """
    def get_timestamp(event: dict[str, Any]) -> str:
        timestamp = event.get('timestamp_utc')
        if not isinstance(timestamp, str):
            raise ValueError(f'event missing or invalid timestamp_utc: {event}')
        try:
            from datetime import datetime
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return timestamp
        except ValueError:
            raise ValueError(f'invalid ISO timestamp_utc in event: {event}')

    return sorted(events, key=get_timestamp)
