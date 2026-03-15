# generated_from: behaviors/load
# spec_hash: 0b934202a49f4432570d0cc3738b0361a1088861a4ceeb405e5962435271ca4f
# generated_at: 2026-03-15T02:31:41.320997+00:00
# agent: implementation-agent
import pytest
from behaviors.sorter import sort_events


class TestSortEvents:
    def test_sorts_by_timestamp_ascending(self):
        events = [
            {'event_id': '3', 'timestamp_utc': '2023-01-02T09:00:00Z'},
            {'event_id': '1', 'timestamp_utc': '2023-01-01T10:00:00Z'},
            {'event_id': '2', 'timestamp_utc': '2023-01-01T11:00:00Z'},
        ]
        sorted_events = sort_events(events)
        timestamps = [e['timestamp_utc'] for e in sorted_events]
        assert timestamps == [
            '2023-01-01T10:00:00Z',
            '2023-01-01T11:00:00Z',
            '2023-01-02T09:00:00Z',
        ]

    def test_missing_timestamp(self):
        events = [{'event_id': '1'}]
        with pytest.raises(ValueError, match='missing or invalid timestamp_utc'):
            sort_events(events)

    def test_invalid_iso_timestamp(self):
        events = [{'event_id': '1', 'timestamp_utc': 'invalid'}]
        with pytest.raises(ValueError, match='invalid ISO timestamp_utc'):
            sort_events(events)

    def test_stable_sort_identical_timestamps(self):
        events = [
            {'event_id': '2', 'timestamp_utc': '2023-01-01T10:00:00Z'},
            {'event_id': '1', 'timestamp_utc': '2023-01-01T10:00:00Z'},
        ]
        sorted_events = sort_events(events)
        assert [e['event_id'] for e in sorted_events] == ['2', '1']
