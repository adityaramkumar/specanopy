# generated_from: behaviors/transform
# spec_hash: b23f1b9a2a7857231ad8294350b7954c38e2dfeb90460a03b6e6ac8603bea4ac
# generated_at: 2026-03-15T02:32:31.303785+00:00
# agent: implementation-agent
def transform(input_dir: str, output_dir: str) -> dict:
    """
    Transform raw events from input directory to processed events in output directory.

    Reads from input_dir/valid/events.ndjson, processes events, and writes partitioned
    output to output_dir/{date}/events.ndjson.

    Args:
        input_dir: Directory containing valid/events.ndjson
        output_dir: Directory to write partitioned processed events

    Returns:
        Summary dict with {"count": int} of processed events

    Raises:
        FileNotFoundError: If input_dir or input_dir/valid/events.ndjson not found
        ValueError: If no valid events found
    """
    from .io import read_valid_events
    from .processing import process_event, compare_events_by_timestamp
    from .io import write_partitioned_events

    raw_events = read_valid_events(input_dir)
    if not raw_events:
        raise ValueError("no valid events found")

    processed_events = [process_event(raw) for raw in raw_events]
    processed_events.sort(key=lambda e: e.timestamp_utc)

    write_partitioned_events(output_dir, processed_events)

    return {"count": len(processed_events)}


def main():
    """CLI entrypoint for transform behavior."""
    import sys
    from pathlib import Path

    if len(sys.argv) != 3:
        print("Usage: python -m behaviors.transform <input_dir> <output_dir>", file=sys.stderr)
        sys.exit(1)

    input_dir, output_dir = sys.argv[1:]

    try:
        result = transform(input_dir, output_dir)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
