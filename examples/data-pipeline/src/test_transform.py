# generated_from: behaviors/transform
# spec_hash: b23f1b9a2a7857231ad8294350b7954c38e2dfeb90460a03b6e6ac8603bea4ac
# generated_at: 2026-03-15T02:32:31.311145+00:00
# agent: testing-agent
# test_transform.py
import pytest
import os
import shutil
from pathlib import Path
from transform import transform

@pytest.fixture
def setup_dirs(tmp_path: Path):
    input_dir = tmp_path / "input"
    valid_dir = input_dir / "valid"
    events_file = valid_dir / "events.ndjson"
    
    input_dir.mkdir()
    valid_dir.mkdir()
    
    return input_dir, events_file

@pytest.fixture
def sample_raw_events():
    return [
        {
            "event_id": "123e4567-e89b-12d3-a456-426614174000",
            "event_type": "page_view",
            "timestamp": "2023-01-01T10:30:00+01:00",
            "user_id": None,
            "properties": {"page": "/home"},
            "source": "web"
        },
        {
            "event_id": "123e4567-e89b-12d3-a456-426614174001",
            "event_type": "click",
            "timestamp": "2023-01-01T11:45:00+02:00",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "properties": {"button": "signup"},
            "source": "web"
        }
    ]

class TestTransformHappyPath:
    def test_transform_processes_valid_events(self, setup_dirs, sample_raw_events):
        input_dir, events_file = setup_dirs
        output_dir = Path(setup_dirs[0]).parent / "output"
        
        # Write sample events
        events_file.write_text("\n".join([str(event) for event in sample_raw_events]) + "\n")
        
        # Execute transform
        result = transform(str(input_dir), str(output_dir))
        
        assert result == {"count": 2}
        
        # Verify output files exist
        output_file = output_dir / "2023-01-01" / "events.ndjson"
        assert output_file.exists()
        
        # Verify events were processed and sorted
        output_content = output_file.read_text().strip().split("\n")
        assert len(output_content) == 2
        
        first_event = eval(output_content[0])
        second_event = eval(output_content[1])
        
        # First event (anonymous, earlier UTC time)
        assert first_event["timestamp_utc"] == "2023-01-01T09:30:00"
        assert first_event["date"] == "2023-01-01"
        assert first_event["hour"] == 9
        assert first_event["user_id"] == "anonymous"
        assert first_event["is_anonymous"] == True
        
        # Second event (identified, later UTC time)
        assert second_event["timestamp_utc"] == "2023-01-01T09:45:00"
        assert second_event["date"] == "2023-01-01"
        assert second_event["hour"] == 9
        assert second_event["user_id"] == "550e8400-e29b-41d4-a716-446655440000"
        assert second_event["is_anonymous"] == False
        
        # Verify sorting by timestamp_utc
        assert first_event["timestamp_utc"] < second_event["timestamp_utc"]

class TestTransformErrorHandling:
    def test_input_dir_not_found_raises_FileNotFoundError(self, tmp_path: Path):
        input_dir = tmp_path / "nonexistent"
        output_dir = tmp_path / "output"
        
        with pytest.raises(FileNotFoundError):
            transform(str(input_dir), str(output_dir))

    def test_valid_events_file_not_found_raises_FileNotFoundError(self, tmp_path: Path):
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        
        with pytest.raises(FileNotFoundError):
            transform(str(input_dir), str(output_dir))

    def test_no_valid_events_raises_ValueError(self, tmp_path: Path):
        input_dir = tmp_path / "input"
        valid_dir = input_dir / "valid"
        events_file = valid_dir / "events.ndjson"
        
        input_dir.mkdir()
        valid_dir.mkdir()
        events_file.touch()  # Empty file
        output_dir = tmp_path / "output"
        
        with pytest.raises(ValueError, match="no valid events found"):
            transform(str(input_dir), str(output_dir))

    def test_empty_events_file_raises_ValueError(self, tmp_path: Path):
        input_dir = tmp_path / "input"
        valid_dir = input_dir / "valid"
        events_file = valid_dir / "events.ndjson"
        
        input_dir.mkdir()
        valid_dir.mkdir()
        events_file.write_text("")  # Empty content
        output_dir = tmp_path / "output"
        
        with pytest.raises(ValueError, match="no valid events found"):
            transform(str(input_dir), str(output_dir))

class TestTransformEdgeCases:
    def test_single_event_transform(self, setup_dirs, tmp_path: Path):
        input_dir, events_file = setup_dirs
        output_dir = tmp_path / "output"
        
        single_event = [
            {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "event_type": "page_view",
                "timestamp": "2023-12-31T23:59:59Z",
                "user_id": None,
                "properties": {},
                "source": "web"
            }
        ]
        
        events_file.write_text("\n".join([str(event) for event in single_event]) + "\n")
        
        result = transform(str(input_dir), str(output_dir))
        
        assert result == {"count": 1}
        output_file = output_dir / "2023-12-31" / "events.ndjson"
        assert output_file.exists()
        
        processed_event = eval(output_file.read_text().strip())
        assert processed_event["hour"] == 23
        assert processed_event["is_anonymous"] == True

    def test_multiple_dates_creates_partitions(self, setup_dirs, tmp_path: Path):
        input_dir, events_file = setup_dirs
        output_dir = tmp_path / "output"
        
        multi_date_events = [
            {
                "event_id": "1",
                "event_type": "page_view",
                "timestamp": "2023-01-01T10:00:00Z",
                "user_id": None,
                "properties": {},
                "source": "web"
            },
            {
                "event_id": "2",
                "event_type": "page_view",
                "timestamp": "2023-01-02T10:00:00Z",
                "user_id": None,
                "properties": {},
                "source": "web"
            }
        ]
        
        events_file.write_text("\n".join([str(event) for event in multi_date_events]) + "\n")
        
        result = transform(str(input_dir), str(output_dir))
        
        assert result == {"count": 2}
        
        jan1_file = output_dir / "2023-01-01" / "events.ndjson"
        jan2_file = output_dir / "2023-01-02" / "events.ndjson"
        
        assert jan1_file.exists()
        assert jan2_file.exists()
