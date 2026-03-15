# generated_from: behaviors/load
# spec_hash: 0b934202a49f4432570d0cc3738b0361a1088861a4ceeb405e5962435271ca4f
# generated_at: 2026-03-15T02:31:41.320556+00:00
# agent: implementation-agent
import pytest
import os
import json
from behaviors.partitioner import partition_events, write_partition


@pytest.fixture
 def sample_events():
    return [
        {'event_id': '1', 'date': '2023-01-01', 'timestamp_utc': '2023-01-01T10:00:00Z'},
        {'event_id': '2', 'date': '2023-01-01', 'timestamp_utc': '2023-01-01T11:00:00Z'},
        {'event_id': '3', 'date': '2023-01-02', 'timestamp_utc': '2023-01-02T09:00:00Z'},
    ]


class TestPartitionEvents:
    def test_partitions_by_date(self, sample_events):
        partitions = partition_events(sample_events, '/tmp')
        assert set(partitions.keys()) == {'2023-01-01', '2023-01-02'}
        assert len(partitions['2023-01-01']) == 2
        assert len(partitions['2023-01-02']) == 1

    def test_missing_date_field(self):
        events = [{'event_id': '1'}]
        with pytest.raises(ValueError, match='missing or invalid date field'):
            partition_events(events, '/tmp')


class TestWritePartition:
    def test_writes_partition(self, tmp_path, sample_events):
        date_events = sample_events[:2]  # First two events (same date)
        write_partition('2023-01-01', date_events, str(tmp_path))

        partition_dir = tmp_path / '2023-01-01'
        assert partition_dir.exists()
        events_file = partition_dir / 'events.ndjson'
        assert events_file.exists()

        read_events = []
        with open(events_file) as f:
            for line in f:
                read_events.append(json.loads(line))
        assert len(read_events) == 2

    def test_write_permission_error(self, tmp_path, sample_events):
        # Make tmp_path read-only
        tmp_path.chmod(0o444)
        try:
            with pytest.raises(OSError):
                write_partition('2023-01-01', sample_events, str(tmp_path))
        finally:
            tmp_path.chmod(0o755)
