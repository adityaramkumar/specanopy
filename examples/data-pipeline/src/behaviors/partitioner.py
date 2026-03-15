# generated_from: behaviors/load
# spec_hash: 0b934202a49f4432570d0cc3738b0361a1088861a4ceeb405e5962435271ca4f
# generated_at: 2026-03-15T02:31:41.318528+00:00
# agent: implementation-agent
import os
import json


def partition_events(events: list[dict[str, any]], output_dir: str) -> dict[str, list[dict[str, any]]]:
    """
    Partition events by 'date' field into date-keyed dictionaries.

    Args:
        events: List of processed events
        output_dir: Base output directory (for reference)

    Returns:
        dict[str, list[dict[str, any]]]: {date: [events]} mapping

    Raises:
        ValueError: If any event missing 'date' field
    """
    partitions: dict[str, list[dict[str, any]]] = {}
    for event in events:
        date = event.get('date')
        if not isinstance(date, str):
            raise ValueError(f'event missing or invalid date field: {event}')
        if date not in partitions:
            partitions[date] = []
        partitions[date].append(event)
    return partitions


def write_partition(date: str, events: list[dict[str, any]], output_dir: str) -> None:
    """
    Write sorted events for a date partition to output_dir/{date}/events.ndjson.

    Args:
        date: Partition date (YYYY-MM-DD)
        events: Sorted events for this partition
        output_dir: Base output directory

    Raises:
        OSError: If cannot create directory or write file
    """
    partition_dir = os.path.join(output_dir, date)
    os.makedirs(partition_dir, exist_ok=True)
    file_path = os.path.join(partition_dir, 'events.ndjson')
    try:
        with open(file_path, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
    except OSError as e:
        raise OSError(f'failed to write partition {date} to {file_path}: {e}')
