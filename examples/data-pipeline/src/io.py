# generated_from: behaviors/transform
# spec_hash: b23f1b9a2a7857231ad8294350b7954c38e2dfeb90460a03b6e6ac8603bea4ac
# generated_at: 2026-03-15T02:32:31.309704+00:00
# agent: implementation-agent
from typing import List, Iterator
from pathlib import Path
import json
import os
from .events import RawEvent, validate_raw_event
from .processing import compare_events_by_timestamp


def read_ndjson(file_path: str) -> Iterator[dict]:
    """
    Read NDJSON file line-by-line as dicts.

    Args:
        file_path: Path to NDJSON file

    Yields:
        Dict per line

    Raises:
        FileNotFoundError: If file_path not found
        ValueError: If line is not valid JSON
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f'NDJSON file not found: {file_path}')

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f'invalid JSON at line {line_num}: {e}')


def read_valid_events(input_dir: str) -> List[RawEvent]:
    """
    Read and validate events from input_dir/valid/events.ndjson.

    Args:
        input_dir: Input directory

    Returns:
        List of validated RawEvent

    Raises:
        FileNotFoundError: If input_dir/valid/events.ndjson not found
        ValueError: If no valid events found
    """
    input_path = Path(input_dir) / 'valid' / 'events.ndjson'
    if not input_path.exists():
        raise FileNotFoundError(f'valid events file not found: {input_path}')

    events = []
    for data in read_ndjson(str(input_path)):
        try:
            event = validate_raw_event(data)
            events.append(event)
        except ValueError:
            # Invalid events are ignored per spec (routed to dead-letter implicitly)
            pass

    if not events:
        raise ValueError("no valid events found")

    return events


def write_partitioned_events(output_dir: str, events: List[ProcessedEvent]) -> None:
    """
    Write processed events to date-partitioned NDJSON files, sorted by timestamp_utc.

    Args:
        output_dir: Output directory
        events: List of ProcessedEvent

    Raises:
        OSError: If output_dir cannot be created or written to
    """
    # Sort events by timestamp_utc
    events.sort(key=lambda e: e.timestamp_utc)

    # Group by date
    events_by_date = {}
    for event in events:
        date = event.date
        if date not in events_by_date:
            events_by_date[date] = []
        events_by_date[date].append(event)

    # Write partitioned files
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for date, date_events in events_by_date.items():
        partition_file = ensure_dir(output_dir, date)
        partition_path = Path(partition_file)
        partition_path.parent.mkdir(parents=True, exist_ok=True)

        with open(partition_file, 'w', encoding='utf-8') as f:
            for event in date_events:
                json.dump(event.__dict__, f, default=str)
                f.write('\n')


def ensure_dir(parent_dir: str, date: str) -> str:
    """
    Create and return path for date-partitioned directory.

    Args:
        parent_dir: Base output directory
        date: YYYY-MM-DD date string

    Returns:
        Full path to {parent_dir}/{date}/events.ndjson
    """
    return str(Path(parent_dir) / date / 'events.ndjson')
