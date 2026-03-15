# generated_from: contracts/schemas/processed
# spec_hash: aa16370c504b0bb024d13816449c4fa02a1383a6f8b296b1bb744bc743ac33db
# generated_at: 2026-03-15T02:31:00.529511+00:00
# agent: testing-agent
import pytest
from datetime import datetime
import uuid
from typing import Dict, Any

from processed_event import ProcessedEvent, parse_processed_event, serialize_processed_event


class TestProcessedEventValidation:
    def test_valid_processed_event_passes_validation(self):
        event_data = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'page_view',
            'timestamp_utc': '2023-10-01T12:34:56.789Z',
            'date': '2023-10-01',
            'hour': 12,
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'web',
            'properties': {'page': '/home'}
        }
        event = ProcessedEvent(**event_data)
        assert event.event_id == event_data['event_id']
        assert event.event_type == 'page_view'
        assert event.is_anonymous is False

    def test_invalid_event_id_uuid_raises_value_error(self):
        event_data = {
            'event_id': 'invalid-uuid',
            'event_type': 'page_view',
            'timestamp_utc': '2023-10-01T12:34:56Z',
            'date': '2023-10-01',
            'hour': 12,
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'web',
            'properties': {}
        }
        with pytest.raises(ValueError, match='event_id must be a valid UUID'):
            ProcessedEvent(**event_data)

    def test_invalid_timestamp_utc_raises_value_error(self):
        event_data = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'page_view',
            'timestamp_utc': 'invalid-date',
            'date': '2023-10-01',
            'hour': 12,
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'web',
            'properties': {}
        }
        with pytest.raises(ValueError, match='timestamp_utc must be valid ISO 8601 UTC'):
            ProcessedEvent(**event_data)

    def test_invalid_date_format_raises_value_error(self):
        event_data = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'page_view',
            'timestamp_utc': '2023-10-01T12:34:56Z',
            'date': '2023/10/01',
            'hour': 12,
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'web',
            'properties': {}
        }
        with pytest.raises(ValueError, match='date must be YYYY-MM-DD format'):
            ProcessedEvent(**event_data)

    def test_hour_outside_range_raises_value_error(self):
        event_data = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'page_view',
            'timestamp_utc': '2023-10-01T12:34:56Z',
            'date': '2023-10-01',
            'hour': 25,
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'web',
            'properties': {}
        }
        with pytest.raises(ValueError, match='hour must be integer between 0-23'):
            ProcessedEvent(**event_data)

    def test_non_integer_hour_raises_value_error(self):
        event_data = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'page_view',
            'timestamp_utc': '2023-10-01T12:34:56Z',
            'date': '2023-10-01',
            'hour': '12',
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'web',
            'properties': {}
        }
        with pytest.raises(ValueError, match='hour must be integer between 0-23'):
            ProcessedEvent(**event_data)

    def test_extra_fields_are_forbidden(self):
        event_data = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'page_view',
            'timestamp_utc': '2023-10-01T12:34:56Z',
            'date': '2023-10-01',
            'hour': 12,
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'web',
            'properties': {},
            'extra_field': 'should fail'
        }
        with pytest.raises(ValueError):
            ProcessedEvent(**event_data)

    def test_anonymous_user_validation(self):
        event_data = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'page_view',
            'timestamp_utc': '2023-10-01T12:34:56Z',
            'date': '2023-10-01',
            'hour': 12,
            'user_id': 'anonymous',
            'is_anonymous': True,
            'source': 'web',
            'properties': {}
        }
        event = ProcessedEvent(**event_data)
        assert event.user_id == 'anonymous'
        assert event.is_anonymous is True


class TestParseProcessedEvent:
    def test_parse_valid_data_returns_processed_event(self):
        raw_data: Dict[str, Any] = {
            'event_id': str(uuid.uuid4()),
            'event_type': 'click',
            'timestamp_utc': '2023-10-02T14:20:30.123Z',
            'date': '2023-10-02',
            'hour': 14,
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'mobile',
            'properties': {'button': 'submit'}
        }
        event = parse_processed_event(raw_data)
        assert isinstance(event, ProcessedEvent)
        assert event.event_type == 'click'

    def test_parse_invalid_data_raises_value_error(self):
        invalid_data = {
            'event_id': 'invalid',
            'event_type': 'page_view',
            'timestamp_utc': '2023-10-01T12:34:56Z',
            'date': '2023-10-01',
            'hour': 12,
            'user_id': str(uuid.uuid4()),
            'is_anonymous': False,
            'source': 'web',
            'properties': {}
        }
        with pytest.raises(ValueError):
            parse_processed_event(invalid_data)


class TestSerializeProcessedEvent:
    def test_serialize_roundtrip_preserves_data(self):
        original_event = ProcessedEvent(
            event_id=str(uuid.uuid4()),
            event_type='purchase',
            timestamp_utc='2023-10-03T09:15:22.456Z',
            date='2023-10-03',
            hour=9,
            user_id=str(uuid.uuid4()),
            is_anonymous=False,
            source='web',
            properties={'amount': 99.99, 'currency': 'USD'}
        )
        serialized = serialize_processed_event(original_event)
        assert serialized['event_id'] == original_event.event_id
        assert serialized['properties'] == original_event.properties
        assert isinstance(serialized, dict)

    def test_serialize_maintains_all_fields(self):
        event = ProcessedEvent(
            event_id=str(uuid.uuid4()),
            event_type='page_view',
            timestamp_utc='2023-10-01T00:00:00Z',
            date='2023-10-01',
            hour=0,
            user_id='anonymous',
            is_anonymous=True,
            source='api',
            properties={}
        )
        serialized = serialize_processed_event(event)
        assert set(serialized.keys()) == {
            'event_id', 'event_type', 'timestamp_utc', 'date', 'hour',
            'user_id', 'is_anonymous', 'source', 'properties'
        }
