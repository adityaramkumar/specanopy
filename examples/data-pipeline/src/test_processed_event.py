# generated_from: contracts/schemas/processed
# spec_hash: aa16370c504b0bb024d13816449c4fa02a1383a6f8b296b1bb744bc743ac33db
# generated_at: 2026-03-15T02:31:00.527975+00:00
# agent: implementation-agent
import pytest
from datetime import datetime
import uuid
from typing import Any, Dict

from processed_event import ProcessedEvent, parse_processed_event, serialize_processed_event


@pytest.fixture
def valid_event_data() -> Dict[str, Any]:
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "page_view",
        "timestamp_utc": "2023-10-15T14:30:45.123Z",
        "date": "2023-10-15",
        "hour": 14,
        "user_id": str(uuid.uuid4()),
        "is_anonymous": False,
        "source": "web",
        "properties": {"page": "/home", "duration": 30.5}
    }


@pytest.fixture
def anonymous_event_data() -> Dict[str, Any]:
    data = valid_event_data()
    data["user_id"] = "anonymous"
    data["is_anonymous"] = True
    return data


def test_valid_event(valid_event_data: Dict[str, Any]):
    event = parse_processed_event(valid_event_data)
    assert event.event_id == valid_event_data["event_id"]
    assert event.event_type == "page_view"
    assert event.is_anonymous is False


def test_anonymous_event(anonymous_event_data: Dict[str, Any]):
    event = parse_processed_event(anonymous_event_data)
    assert event.user_id == "anonymous"
    assert event.is_anonymous is True


def test_serialize_roundtrip(valid_event_data: Dict[str, Any]):
    event = parse_processed_event(valid_event_data)
    serialized = serialize_processed_event(event)
    assert serialized == valid_event_data


def test_invalid_event_id(valid_event_data: Dict[str, Any]):
    valid_event_data["event_id"] = "invalid-uuid"
    with pytest.raises(ValueError, match="event_id must be a valid UUID"):
        parse_processed_event(valid_event_data)


def test_invalid_timestamp(valid_event_data: Dict[str, Any]):
    valid_event_data["timestamp_utc"] = "invalid-date"
    with pytest.raises(ValueError, match="timestamp_utc must be valid ISO 8601 UTC"):
        parse_processed_event(valid_event_data)


def test_invalid_date(valid_event_data: Dict[str, Any]):
    valid_event_data["date"] = "2023/10/15"
    with pytest.raises(ValueError, match="date must be YYYY-MM-DD format"):
        parse_processed_event(valid_event_data)


def test_invalid_hour(valid_event_data: Dict[str, Any]):
    valid_event_data["hour"] = 25
    with pytest.raises(ValueError, match="hour must be integer between 0-23"):
        parse_processed_event(valid_event_data)


def test_extra_fields(valid_event_data: Dict[str, Any]):
    valid_event_data["extra_field"] = "value"
    with pytest.raises(ValueError):
        parse_processed_event(valid_event_data)
