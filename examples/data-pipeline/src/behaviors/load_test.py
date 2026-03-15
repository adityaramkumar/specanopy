# generated_from: behaviors/load
# spec_hash: 0b934202a49f4432570d0cc3738b0361a1088861a4ceeb405e5962435271ca4f
# generated_at: 2026-03-15T02:31:41.320157+00:00
# agent: implementation-agent
import pytest
import os
import json
import shutil
from behaviors.load import load, parse_events


@pytest.fixture
 def sample_events_dir(tmp_path):
    input_dir = tmp_path / 'input'
    input_dir.mkdir()
    events_file = input_dir / 'events.ndjson'
    events = [
        {'event_id': '1', 'event_type': 'click', 'timestamp_utc': '2023-01-01T10:00:00Z', 'date': '2023-01-01', 'user_id': 'user1', 'is_anonymous': False, 'source': 'web', 'properties': {}},
        {'event_id': '2', 'event_type': 'view', 'timestamp_utc': '2023-01-01T11:00:00Z', 'date': '2023-01-01', 'user_id': 'user2', 'is_anonymous': True, 'source': 'mobile', 'properties': {}},
        {'event_id': '3', 'event_type': 'click', 'timestamp_utc': '2023-01-02T09:00:00Z', 'date': '2023-01-02', 'user_id': 'user3', 'is_anonymous': False, 'source': 'web', 'properties': {}},
    ]
    with open(events_file, 'w') as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
    return str(input_dir)


class TestLoad:
    def test_happy_path(self, sample_events_dir, tmp_path):
        output_dir = str(tmp_path / 'output')
        result = load(sample_events_dir, output_dir)
        assert result == {'count': 3, 'partitions': 2}

        # Verify partitions
        date1_dir = os.path.join(output_dir, '2023-01-01')
        date2_dir = os.path.join(output_dir, '2023-01-02')
        assert os.path.exists(date1_dir)
        assert os.path.exists(date2_dir)

        # Verify sorting within partitions
        events_date1 = []
        with open(os.path.join(date1_dir, 'events.ndjson')) as f:
            for line in f:
                events_date1.append(json.loads(line))
        timestamps_date1 = [e['timestamp_utc'] for e in events_date1]
        assert timestamps_date1 == ['2023-01-01T10:00:00Z', '2023-01-01T11:00:00Z']

    def test_input_dir_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load(str(tmp_path / 'missing'), str(tmp_path / 'output'))

    def test_no_events_file(self, tmp_path):
        input_dir = tmp_path / 'input'
        input_dir.mkdir()
        with pytest.raises(ValueError, match='no events found'):
            load(str(input_dir), str(tmp_path / 'output'))


class TestParseEvents:
    def test_valid_ndjson(self, sample_events_dir):
        events_file = os.path.join(sample_events_dir, 'events.ndjson')
        events = parse_events(events_file)
        assert len(events) == 3

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_events('/nonexistent/events.ndjson')

    def test_empty_file(self, tmp_path):
        events_file = tmp_path / 'events.ndjson'
        events_file.write_text('')
        events = parse_events(str(events_file))
        assert events == []

    def test_malformed_json(self, tmp_path):
        events_file = tmp_path / 'events.ndjson'
        events_file.write_text('invalid json')
        with pytest.raises(ValueError, match='malformed JSON'):
            parse_events(str(events_file))
