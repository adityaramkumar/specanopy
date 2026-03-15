# generated_from: behaviors/ingest
# spec_hash: a46bf4c24197a3b855328de74eab6c7676c144c326dc88fd066bc5484a1f8221
# generated_at: 2026-03-15T02:32:11.596301+00:00
# agent: implementation-agent
import pytest
from schemas.raw_events import RawEvent, validate_raw_event
import uuid
from datetime import datetime

@pytest.fixture
def valid_event():
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "page_view",
        "timestamp": "2023-01-01T12:00:00Z",
        "user_id": str(uuid.uuid4()),
        "properties": {"page": "home"},
        "source": "web"
    }

@pytest.fixture
def anonymous_event():
    event = valid_event()
    event["user_id"] = None
    return event

class TestRawEventValidation:
    def test_valid_event_passes(self, valid_event):
        result, error = validate_raw_event(valid_event)
        assert result is not None
        assert error is None
        assert isinstance(result, RawEvent)

    def test_anonymous_event_passes(self, anonymous_event):
        result, error = validate_raw_event(anonymous_event)
        assert result is not None
        assert error is None

    def test_invalid_event_id(self, valid_event):
        valid_event["event_id"] = "invalid-uuid"
        result, error = validate_raw_event(valid_event)
        assert result is None
        assert "event_id" in error

    def test_invalid_event_type(self, valid_event):
        valid_event["event_type"] = "invalid_type"
        result, error = validate_raw_event(valid_event)
        assert result is None
        assert "event_type" in error

    def test_invalid_timestamp(self, valid_event):
        valid_event["timestamp"] = "invalid-timestamp"
        result, error = validate_raw_event(valid_event)
        assert result is None
        assert "timestamp" in error

    def test_invalid_source(self, valid_event):
        valid_event["source"] = "invalid_source"
        result, error = validate_raw_event(valid_event)
        assert result is None
        assert "source" in error

    def test_invalid_properties(self, valid_event):
        valid_event["properties"] = ["not", "a", "dict"]
        result, error = validate_raw_event(valid_event)
        assert result is None
        assert "properties" in error

    def test_extra_field_forbidden(self, valid_event):
        valid_event["extra_field"] = "value"
        result, error = validate_raw_event(valid_event)
        assert result is None
        assert "extra" in error.lower()
