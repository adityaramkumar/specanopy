# generated_from: contracts/schemas/processed
# spec_hash: aa16370c504b0bb024d13816449c4fa02a1383a6f8b296b1bb744bc743ac33db
# generated_at: 2026-03-15T02:31:00.529012+00:00
# agent: implementation-agent
import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import json

from processed_event import ProcessedEvent, parse_processed_event, serialize_processed_event
from partition_writer import write_partitioned_events, get_partition_path


@pytest.fixture
def sample_events() -> list[ProcessedEvent]:
    events_data = [
        {
            "event_id": "550e8400-e29b-41d4-a716-446655440000",
            "event_type": "page_view",
            "timestamp_utc": "2023-10-15T10:30:00Z",
            "date": "2023-10-15",
            "hour": 10,
            "user_id": "user1",
            "is_anonymous": False,
            "source": "web",
            "properties": {"page": "/home"}
        },
        {
            "event_id": "550e8400-e29b-41d4-a716-446655440001",
            "event_type": "click",
            "timestamp_utc": "2023-10-15T11:15:00Z",
            "date": "2023-10-15",
            "hour": 11,
            "user_id": "user1",
            "is_anonymous": False,
            "source": "web",
            "properties": {"button": "submit"}
        },
        {
            "event_id": "550e8400-e29b-41d4-a716-446655440002",
            "event_type": "page_view",
            "timestamp_utc": "2023-10-16T09:45:00Z",
            "date": "2023-10-16",
            "hour": 9,
            "user_id": "user2",
            "is_anonymous": False,
            "source": "mobile",
            "properties": {"page": "/profile"}
        }
    ]
    return [parse_processed_event(data) for data in events_data]


def test_write_partitioned_events(tmp_path: Path, sample_events: list[ProcessedEvent]) -> None:
    result = write_partitioned_events(sample_events, tmp_path)
    
    assert result == {"2023-10-15": 2, "2023-10-16": 1}
    
    # Check 2023-10-15 partition
    path1 = tmp_path / "2023-10-15" / "events.ndjson"
    assert path1.exists()
    lines1 = path1.read_text(encoding='utf-8').strip().split('\n')
    assert len(lines1) == 2
    
    event1 = json.loads(lines1[0])
    event2 = json.loads(lines1[1])
    assert event1["timestamp_utc"] < event2["timestamp_utc"]
    
    # Check 2023-10-16 partition
    path2 = tmp_path / "2023-10-16" / "events.ndjson"
    assert path2.exists()
    lines2 = path2.read_text(encoding='utf-8').strip().split('\n')
    assert len(lines2) == 1


def test_get_partition_path(tmp_path: Path) -> None:
    path = get_partition_path("2023-10-15", tmp_path)
    assert path == tmp_path / "2023-10-15" / "events.ndjson"


def test_empty_events(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="events list cannot be empty"):
        write_partitioned_events([], tmp_path)


def test_empty_output_dir() -> None:
    with pytest.raises(ValueError, match="output_dir cannot be empty"):
        write_partitioned_events([], "")


def test_single_partition(tmp_path: Path, sample_events: list[ProcessedEvent]) -> None:
    # Only events from one date
    single_date_events = [e for e in sample_events if e.date == "2023-10-15"]
    result = write_partitioned_events(single_date_events, tmp_path)
    assert result == {"2023-10-15": 2}
    
    path = tmp_path / "2023-10-15" / "events.ndjson"
    assert path.exists()
    lines = path.read_text(encoding='utf-8').strip().split('\n')
    assert len(lines) == 2
    
    # Verify sorting
    timestamps = [json.loads(line)['timestamp_utc'] for line in lines]
    assert timestamps[0] < timestamps[1]


def test_ndjson_format(tmp_path: Path, sample_events: list[ProcessedEvent]) -> None:
    write_partitioned_events(sample_events, tmp_path)
    
    path = tmp_path / "2023-10-15" / "events.ndjson"
    content = path.read_text(encoding='utf-8')
    
    # Each line should be valid JSON + newline
    lines = content.strip().split('\n')
    for line in lines:
        json.loads(line)
    
    # File should end with newline
    assert content.endswith('\n')