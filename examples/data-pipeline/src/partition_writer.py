# generated_from: contracts/schemas/processed
# spec_hash: aa16370c504b0bb024d13816449c4fa02a1383a6f8b296b1bb744bc743ac33db
# generated_at: 2026-03-15T02:31:00.528551+00:00
# agent: implementation-agent
from datetime import date
from pathlib import Path
from typing import List

from processed_event import ProcessedEvent


def write_partitioned_events(
    events: List[ProcessedEvent],
    output_dir: Path | str,
) -> Dict[str, int]:
    """
    Write sorted processed events to date-partitioned NDJSON files.

    Events are sorted by timestamp_utc ascending within each partition.
    Files are written as {date}/events.ndjson

    Args:
        events: List of processed events
        output_dir: Directory to write partitioned files

    Returns:
        Dictionary mapping date to count of events written

    Raises:
        ValueError: If events list is empty or output_dir is invalid
        PermissionError: If cannot write to output directory
        OSError: If filesystem errors occur
    """
    output_path = Path(output_dir)
    if not output_path:
        raise ValueError("output_dir cannot be empty")

    if not events:
        raise ValueError("events list cannot be empty")

    # Group events by date
    events_by_date: Dict[str, List[ProcessedEvent]] = {}
    for event in events:
        date_key = event.date
        if date_key not in events_by_date:
            events_by_date[date_key] = []
        events_by_date[date_key].append(event)

    date_counts: Dict[str, int] = {}
    for date_str, date_events in events_by_date.items():
        # Sort by timestamp_utc ascending
        date_events.sort(key=lambda e: e.timestamp_utc)
        
        partition_path = get_partition_path(date_str, output_dir)
        partition_path.parent.mkdir(parents=True, exist_ok=True)
        
        with partition_path.open('w', encoding='utf-8') as f:
            for event in date_events:
                line = serialize_processed_event(event) + '\n'
                f.write(line)
        
        date_counts[date_str] = len(date_events)

    return date_counts


def get_partition_path(date_str: str, output_dir: Path | str) -> Path:
    """
    Get the NDJSON file path for a specific date partition.

    Args:
        date_str: Date in YYYY-MM-DD format
        output_dir: Base output directory

    Returns:
        Path to events.ndjson file for that date
    """
    output_path = Path(output_dir)
    return output_path / date_str / "events.ndjson"
