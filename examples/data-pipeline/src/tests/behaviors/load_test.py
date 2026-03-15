# generated_from: behaviors/load
# spec_hash: 0b934202a49f4432570d0cc3738b0361a1088861a4ceeb405e5962435271ca4f
# generated_at: 2026-03-15T02:31:41.321412+00:00
# agent: testing-agent
# Generated unit tests for load behavior (Spec ID: behaviors/load v1.0.1)

import pytest
import os
import tempfile
from pathlib import Path
import shutil
from behaviors.load import load, parse_events


class TestLoadBehavior:
    def setup_method(self):
        self.temp_input = tempfile.mkdtemp()
        self.temp_output = tempfile.mkdtemp()
        self.events_file = os.path.join(self.temp_input, 'events.ndjson')

    def teardown_method(self):
        shutil.rmtree(self.temp_input, ignore_errors=True)
        shutil.rmtree(self.temp_output, ignore_errors=True)

    def write_events_file(self, events):
        with open(self.events_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')

    @pytest.fixture
    def sample_events(self):
        return [
            {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "event_type": "page_view",
                "timestamp_utc": "2023-10-01T10:00:00Z",
                "date": "2023-10-01",
                "hour": 10,
                "user_id": "user-123",
                "is_anonymous": False,
                "source": "web",
                "properties": {"page": "/home"}
            },
            {
                "event_id": "123e4567-e89b-12d3-a456-426614174001",
                "event_type": "click",
                "timestamp_utc": "2023-10-01T10:05:00Z",
                "date": "2023-10-01",
                "hour": 10,
                "user_id": "anonymous",
                "is_anonymous": True,
                "source": "web",
                "properties": {"button": "submit"}
            },
            {
                "event_id": "123e4567-e89b-12d3-a456-426614174002",
                "event_type": "page_view",
                "timestamp_utc": "2023-10-02T14:30:00Z",
                "date": "2023-10-02",
                "hour": 14,
                "user_id": "user-456",
                "is_anonymous": False,
                "source": "mobile",
                "properties": {"page": "/profile"}
            }
        ]

    def test_happy_path_multiple_dates(self, sample_events):
        # Arrange
        self.write_events_file(sample_events)

        # Act
        result = load(self.temp_input, self.temp_output)

        # Assert
        assert result == {"count": 3, "partitions": 2}

        # Verify partitions created
        date1_path = os.path.join(self.temp_output, '2023-10-01', 'events.ndjson')
        date2_path = os.path.join(self.temp_output, '2023-10-02', 'events.ndjson')
        assert os.path.exists(date1_path)
        assert os.path.exists(date2_path)

        # Verify date1 partition: 2 events, sorted by timestamp_utc
        with open(date1_path) as f:
            date1_events = [json.loads(line) for line in f]
        assert len(date1_events) == 2
        assert date1_events[0]['timestamp_utc'] == '2023-10-01T10:00:00Z'
        assert date1_events[1]['timestamp_utc'] == '2023-10-01T10:05:00Z'

        # Verify date2 partition: 1 event
        with open(date2_path) as f:
            date2_events = [json.loads(line) for line in f]
        assert len(date2_events) == 1
        assert date2_events[0]['timestamp_utc'] == '2023-10-02T14:30:00Z'

    def test_single_partition(self):
        events = [
            {
                "event_id": "1",
                "event_type": "test",
                "timestamp_utc": "2023-10-01T12:00:00Z",
                "date": "2023-10-01",
                "hour": 12,
                "user_id": "user",
                "is_anonymous": False,
                "source": "test",
                "properties": {}
            }
        ]
        self.write_events_file(events)

        result = load(self.temp_input, self.temp_output)
        assert result == {"count": 1, "partitions": 1}

        partition_path = os.path.join(self.temp_output, '2023-10-01', 'events.ndjson')
        assert os.path.exists(partition_path)

    def test_input_directory_not_found(self):
        with pytest.raises(FileNotFoundError):
            load('/nonexistent/input', self.temp_output)

    def test_no_events_file(self):
        os.makedirs(self.temp_input, exist_ok=True)
        with pytest.raises(ValueError, match="no events found"):
            load(self.temp_input, self.temp_output)

    def test_empty_events_file(self):
        os.makedirs(self.temp_input, exist_ok=True)
        Path(self.events_file).touch()
        with pytest.raises(ValueError, match="no events found"):
            load(self.temp_input, self.temp_output)


class TestParseEvents:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.events_file = os.path.join(self.temp_dir, 'events.ndjson')

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def write_events_file(self, events):
        with open(self.events_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')

    def test_parse_valid_ndjson(self):
        events = [{"test": "data"}]
        self.write_events_file(events)
        result = parse_events(self.events_file)
        assert result == events

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_events('/nonexistent.ndjson')

    def test_empty_file(self):
        Path(self.events_file).touch()
        with pytest.raises(ValueError, match="empty or malformed"):
            parse_events(self.events_file)

    def test_malformed_json(self):
        with open(self.events_file, 'w') as f:
            f.write('invalid json')
        with pytest.raises(ValueError, match="empty or malformed"):
            parse_events(self.events_file)
