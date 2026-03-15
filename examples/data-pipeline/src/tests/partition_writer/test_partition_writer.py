# generated_from: contracts/schemas/processed
# spec_hash: aa16370c504b0bb024d13816449c4fa02a1383a6f8b296b1bb744bc743ac33db
# generated_at: 2026-03-15T02:31:00.530547+00:00
# agent: testing-agent
import pytest
from pathlib import Path
from datetime import date
from typing import List

from processed_event import ProcessedEvent
from partition_writer import write_partitioned_events, get_partition_path


@pytest.fixture
def tmp_output_dir(tmp_path: Path) -> Path:
    return tmp_path / "output"


class TestGetPartitionPath:
    def test_returns_correct_path_for_date_partition(self, tmp_output_dir: Path):
        path = get_partition_path('2023-10-01', tmp_output_dir)
        expected = tmp_output_dir / '2023-10-01' / 'events.ndjson'
        assert path == expected

    def test_handles_string_output_dir(self):
        path = get_partition_path('2023-10-02', str(Path.cwd()))
        expected = Path.cwd() / '2023-10-02' / 'events.ndjson'
        assert path == expected

    def test_date_partition_format_is_correct(self, tmp_output_dir: Path):
        path = get_partition_path('2024-01-15', tmp_output_dir)
        assert str(path).endswith('2024-01-15/events.ndjson')


class TestWritePartitionedEvents:
    @pytest.fixture
    def sample_events(self) -> List[ProcessedEvent]:
        return [
            ProcessedEvent(
                event_id='00000000-0000-0000-0000-000000000001',
                event_type='page_view',
                timestamp_utc='2023-10-01T10:00:00Z',
                date='2023-10-01',
                hour=10,
                user_id='user1',
                is_anonymous=False,
                source='web',
                properties={}
            ),
            ProcessedEvent(
                event_id='00000000-0000-0000-0000-000000000002',
                event_type='click',
                timestamp_utc='2023-10-01T11:30:00Z',
                date='2023-10-01',
                hour=11,
                user_id='user1',
                is_anonymous=False,
                source='web',
                properties={'button': 'submit'}
            ),
            ProcessedEvent(
                event_id='00000000-0000-0000-0000-000000000003',
                event_type='page_view',
                timestamp_utc='2023-10-02T09:15:00Z',
                date='2023-10-02',
                hour=9,
                user_id='anonymous',
                is_anonymous=True,
                source='mobile',
                properties={}
            )
        ]

    def test_writes_events_to_date_partitioned_ndjson_files(self, tmp_output_dir: Path, sample_events: List[ProcessedEvent]):
        result = write_partitioned_events(sample_events, tmp_output_dir)
        
        assert '2023-10-01' in result
        assert '2023-10-02' in result
        assert result['2023-10-01'] == 2
        assert result['2023-10-02'] == 1

        # Verify files exist
        assert (tmp_output_dir / '2023-10-01' / 'events.ndjson').exists()
        assert (tmp_output_dir / '2023-10-02' / 'events.ndjson').exists()

    def test_events_within_partition_are_sorted_by_timestamp_utc(self, tmp_output_dir: Path, sample_events: List[ProcessedEvent]):
        # Events are already in order, but test with unsorted events
        unsorted_events = sample_events[::-1]  # Reverse order
        write_partitioned_events(unsorted_events, tmp_output_dir)
        
        file_path = tmp_output_dir / '2023-10-01' / 'events.ndjson'
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            events = [ProcessedEvent.parse_raw(line) for line in lines]
            
            # Verify sorted by timestamp_utc ascending
            timestamps = [event.timestamp_utc for event in events]
            assert timestamps == sorted(timestamps)

    def test_empty_events_list_raises_value_error(self, tmp_output_dir: Path):
        with pytest.raises(ValueError, match='events list is empty'):
            write_partitioned_events([], tmp_output_dir)

    def test_invalid_output_dir_raises_value_error(self, sample_events: List[ProcessedEvent]):
        invalid_dir = '/nonexistent/invalid/path'
        with pytest.raises((ValueError, PermissionError)):
            write_partitioned_events(sample_events, invalid_dir)

    def test_single_partition_single_event(self, tmp_output_dir: Path):
        events = [
            ProcessedEvent(
                event_id='11111111-1111-1111-1111-111111111111',
                event_type='test',
                timestamp_utc='2023-12-25T12:00:00Z',
                date='2023-12-25',
                hour=12,
                user_id='test-user',
                is_anonymous=False,
                source='test',
                properties={'key': 'value'}
            )
        ]
        result = write_partitioned_events(events, tmp_output_dir)
        assert result == {'2023-12-25': 1}
        file_path = tmp_output_dir / '2023-12-25' / 'events.ndjson'
        assert file_path.exists()
