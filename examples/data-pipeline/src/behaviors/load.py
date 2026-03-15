# generated_from: behaviors/load
# spec_hash: 0b934202a49f4432570d0cc3738b0361a1088861a4ceeb405e5962435271ca4f
# generated_at: 2026-03-15T02:31:41.315541+00:00
# agent: implementation-agent
def load(input_dir: str, output_dir: str) -> dict:
    """
    Load processed events from input_dir/events.ndjson, partition by date,
    and write sorted events to output_dir/{date}/events.ndjson.

    Args:
        input_dir: Directory containing events.ndjson
        output_dir: Directory to write partitioned events

    Returns:
        dict: {"count": int, "partitions": int}

    Raises:
        FileNotFoundError: If input_dir or events.ndjson not found
        ValueError: If no events found
    """
    events_file = f'{input_dir}/events.ndjson'
    events = parse_events(events_file)
    if not events:
        raise ValueError('no events found')

    sorted_events = sort_events(events)
    partitions = partition_events(sorted_events, output_dir)

    total_count = sum(len(events_list) for events_list in partitions.values())
    return {'count': total_count, 'partitions': len(partitions)}


def parse_events(file_path: str) -> list[dict[str, any]]:
    """
    Parse NDJSON events file into list of event dicts.

    Args:
        file_path: Path to events.ndjson

    Returns:
        list[dict[str, any]]: List of parsed events

    Raises:
        FileNotFoundError: If file_path not found
        ValueError: If file is empty or malformed
    """
    try:
        with open(file_path, 'r') as f:
            events = []
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    events.append(event)
                except json.JSONDecodeError as e:
                    raise ValueError(f'malformed JSON at line {line_num}: {e}')
            return events
    except FileNotFoundError:
        raise FileNotFoundError(f'events file not found: {file_path}')
