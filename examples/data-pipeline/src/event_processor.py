# generated_from: behaviors/ingest
# spec_hash: a46bf4c24197a3b855328de74eab6c7676c144c326dc88fd066bc5484a1f8221
# generated_at: 2026-03-15T02:32:11.595391+00:00
# agent: implementation-agent
from pathlib import Path
from typing import Iterator
import json
from schemas.raw_events import validate_raw_event

type RawEvent = 'schemas.raw_events.RawEvent'


def process_ndjson_file(
    file_path: Path,
    valid_output: Path,
    dead_letter_output: Path
) -> tuple[int, int]:
    """
    Process single NDJSON file: validate events, write to valid/dead-letter.

    Args:
        file_path: Input NDJSON file
        valid_output: valid/events.ndjson path
        dead_letter_output: dead-letter/events.ndjson path

    Returns:
        Tuple of (valid_count, invalid_count)

    Raises:
        None
    """
    from file_utils import read_ndjson_lines
    
    valid_count = 0
    invalid_count = 0
    
    for event_json in read_ndjson_lines(file_path):
        validated, error = validate_raw_event(event_json)
        
        if validated:
            write_event_valid(validated, valid_output)
            valid_count += 1
        else:
            write_event_dead_letter(event_json, error, dead_letter_output)
            invalid_count += 1
    
    return valid_count, invalid_count


def write_event_valid(event: RawEvent, output_path: Path) -> None:
    """
    Append validated event to valid output file.

    Args:
        event: Validated RawEvent
        output_path: valid/events.ndjson path

    Raises:
        IOError: if write fails
    """
    event_json = event.dict()
    try:
        with output_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(event_json) + '\n')
    except IOError as e:
        raise IOError(f"Failed to write to {output_path}: {e}")


def write_event_dead_letter(event_json: dict, error: str, output_path: Path) -> None:
    """
    Append invalid event with _error field to dead-letter output.

    Args:
        event_json: Original invalid event dict
        error: Validation error message
        output_path: dead-letter/events.ndjson path

    Raises:
        IOError: if write fails
    """
    dead_letter_event = event_json.copy()
    dead_letter_event['_error'] = error
    
    try:
        with output_path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(dead_letter_event) + '\n')
    except IOError as e:
        raise IOError(f"Failed to write to {output_path}: {e}")
