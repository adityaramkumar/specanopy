# generated_from: contracts/schemas/raw-events
# spec_hash: 85ff15643dade015b7da1836a539898f4bf3ba1c18eca0ca704255f3b1f21ad3
# generated_at: 2026-03-15T02:31:17.891822+00:00
# agent: testing-agent
# Generated unit tests for contracts/schemas/raw-events

import pytest
from typing import Dict, Any
from datetime import datetime, timezone

import uuid

from schemas import RawEvent, EventType, Source, validate_raw_event, validate_ndjson_events


class TestEventTypeEnum:
    def test_valid_event_types(self):
        assert EventType.PAGE_VIEW == "page_view"
        assert EventType.CLICK == "click"
        assert EventType.PURCHASE == "purchase"
        assert EventType.SIGNUP == "signup"


class TestSourceEnum:
    def test_valid_sources(self):
        assert Source.WEB == "web"
        assert Source.MOBILE == "mobile"
        assert Source.API == "api"


class TestRawEventValidation:
    @pytest.fixture
    def valid_event_dict(self) -> Dict[str, Any]:
        return {
            "event_id": "550e8400-e29b-41d4-a716-446655440000",
            "event_type": "page_view",
            "timestamp": "2023-10-01T12:00:00Z",
            "user_id": "550e8400-e29b-41d4-a716-446655440001",
            "properties": {"page": "home"},
            "source": "web"
        }

    def test_valid_event_passes_validation(self, valid_event_dict: Dict[str, Any]):
        # WHEN
        result = validate_raw_event(valid_event_dict)
        # THEN
        assert isinstance(result, RawEvent)
        assert result.event_id == valid_event_dict["event_id"]
        assert result.event_type == EventType.PAGE_VIEW
        assert result.timestamp == "2023-10-01T12:00:00Z"
        assert result.user_id == valid_event_dict["user_id"]
        assert result.properties == {"page": "home"}
        assert result.source == Source.WEB

    def test_valid_anonymous_event_passes_validation(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        event_dict["user_id"] = None
        # WHEN
        result = validate_raw_event(event_dict)
        # THEN
        assert result.user_id is None

    def test_invalid_event_id_raises_value_error(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        event_dict["event_id"] = "invalid-uuid"
        # THEN
        with pytest.raises(ValueError, match="event_id must be a valid UUID"):
            validate_raw_event(event_dict)

    def test_missing_event_id_raises_validation_error(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        del event_dict["event_id"]
        # THEN
        with pytest.raises(ValueError):
            validate_raw_event(event_dict)

    def test_invalid_event_type_raises_validation_error(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        event_dict["event_type"] = "invalid_type"
        # THEN
        with pytest.raises(ValueError):
            validate_raw_event(event_dict)

    def test_valid_iso8601_timestamps_pass(self):
        timestamps = [
            "2023-10-01T12:00:00Z",
            "2023-10-01T12:00:00+00:00",
            "2023-10-01T12:00:00.123Z",
            "2023-10-01T12:00:00+02:00"
        ]
        for ts in timestamps:
            event_dict = {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "page_view",
                "timestamp": ts,
                "properties": {"test": True},
                "source": "web"
            }
            result = validate_raw_event(event_dict)
            assert result.timestamp == ts

    def test_invalid_timestamp_raises_value_error(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        event_dict["timestamp"] = "invalid-date"
        # THEN
        with pytest.raises(ValueError, match="timestamp must be valid ISO 8601 format"):
            validate_raw_event(event_dict)

    def test_missing_timestamp_raises_validation_error(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        del event_dict["timestamp"]
        # THEN
        with pytest.raises(ValueError):
            validate_raw_event(event_dict)

    def test_properties_must_be_dict(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        event_dict["properties"] = ["not", "a", "dict"]
        # THEN
        with pytest.raises(ValueError, match="properties must be a dictionary"):
            validate_raw_event(event_dict)

    def test_properties_null_fails(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        event_dict["properties"] = None
        # THEN
        with pytest.raises(ValueError, match="properties must be a dictionary"):
            validate_raw_event(event_dict)

    def test_invalid_source_raises_validation_error(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        event_dict["source"] = "invalid_source"
        # THEN
        with pytest.raises(ValueError):
            validate_raw_event(event_dict)

    def test_missing_source_raises_validation_error(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        del event_dict["source"]
        # THEN
        with pytest.raises(ValueError):
            validate_raw_event(event_dict)

    def test_extra_fields_are_forbidden(self, valid_event_dict: Dict[str, Any]):
        # GIVEN
        event_dict = valid_event_dict.copy()
        event_dict["extra_field"] = "should fail"
        # THEN
        with pytest.raises(ValueError):
            validate_raw_event(event_dict)


class TestNDJSONValidation:
    def test_single_valid_event(self):
        # GIVEN
        ndjson_data = '{"event_id":"550e8400-e29b-41d4-a716-446655440000","event_type":"page_view","timestamp":"2023-10-01T12:00:00Z","properties":{"page":"home"},"source":"web"}'
        # WHEN
        result = validate_ndjson_events(ndjson_data)
        # THEN
        assert len(result) == 1
        assert isinstance(result[0], RawEvent)

    def test_multiple_valid_events(self):
        # GIVEN
        ndjson_data = """{"event_id":"550e8400-e29b-41d4-a716-446655440000","event_type":"page_view","timestamp":"2023-10-01T12:00:00Z","properties":{"page":"home"},"source":"web"}
{"event_id":"550e8400-e29b-41d4-a716-446655440001","event_type":"click","timestamp":"2023-10-01T12:01:00Z","properties":{"button":"cta"},"source":"mobile"}"""
        # WHEN
        result = validate_ndjson_events(ndjson_data)
        # THEN
        assert len(result) == 2
        assert all(isinstance(event, RawEvent) for event in result)

    def test_invalid_json_raises_value_error(self):
        # GIVEN
        ndjson_data = "invalid json"
        # THEN
        with pytest.raises(ValueError):
            validate_ndjson_events(ndjson_data)

    def test_ndjson_with_invalid_event_raises_value_error(self):
        # GIVEN
        ndjson_data = '{"event_id":"invalid-uuid","event_type":"page_view","timestamp":"2023-10-01T12:00:00Z","properties":{"page":"home"},"source":"web"}'
        # THEN
        with pytest.raises(ValueError, match="event_id must be a valid UUID"):
            validate_ndjson_events(ndjson_data)

    def test_empty_ndjson_returns_empty_list(self):
        # WHEN
        result = validate_ndjson_events("")
        # THEN
        assert result == []

    def test_ndjson_with_only_whitespace_returns_empty_list(self):
        # WHEN
        result = validate_ndjson_events("\n\n  \n\n")
        # THEN
        assert result == []
