# generated_from: behaviors/ingest
# spec_hash: a46bf4c24197a3b855328de74eab6c7676c144c326dc88fd066bc5484a1f8221
# generated_at: 2026-03-15T02:32:11.595875+00:00
# agent: implementation-agent
from typing import Dict
from pathlib import Path
from file_utils import scan_ndjson_files, create_output_dirs
from event_processor import process_ndjson_file


def ingest(input_dir: str, output_dir: str) -> Dict[str, int]:
    """
    Main ingest function: scan, process NDJSON files, validate events.

    Args:
        input_dir: Directory containing *.ndjson files
        output_dir: Directory for valid/ and dead-letter/ outputs

    Returns:
        Summary dict: {"valid": int, "invalid": int, "files": int}

    Raises:
        FileNotFoundError: if input_dir doesn't exist
        ValueError: if no .ndjson files found
    """
    ndjson_files = scan_ndjson_files(input_dir)
    valid_dir, dead_letter_dir = create_output_dirs(output_dir)
    
    valid_output = valid_dir / "events.ndjson"
    dead_letter_output = dead_letter_dir / "events.ndjson"
    
    total_valid = 0
    total_invalid = 0
    
    for file_path in ndjson_files:
        valid_count, invalid_count = process_ndjson_file(
            file_path, valid_output, dead_letter_output
        )
        total_valid += valid_count
        total_invalid += invalid_count
    
    return {
        "valid": total_valid,
        "invalid": total_invalid,
        "files": len(ndjson_files)
    }
