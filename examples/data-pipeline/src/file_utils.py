# generated_from: behaviors/ingest
# spec_hash: a46bf4c24197a3b855328de74eab6c7676c144c326dc88fd066bc5484a1f8221
# generated_at: 2026-03-15T02:32:11.594726+00:00
# agent: implementation-agent
from typing import List, Iterator
from pathlib import Path
import json
import os


def scan_ndjson_files(input_dir: str) -> List[Path]:
    """
    Scan input directory for *.ndjson files.

    Args:
        input_dir: Path to input directory

    Returns:
        List of Path objects for NDJSON files

    Raises:
        FileNotFoundError: if input_dir does not exist
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    ndjson_files = list(input_path.glob("*.ndjson"))
    if not ndjson_files:
        raise ValueError("no .ndjson files found")
    
    return [f for f in ndjson_files if f.stat().st_size > 0]


def create_output_dirs(output_dir: str) -> tuple[Path, Path]:
    """
    Create valid/ and dead-letter/ subdirectories in output_dir.

    Args:
        output_dir: Path to output directory

    Returns:
        Tuple of (valid_dir, dead_letter_dir) Path objects

    Raises:
        None
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    valid_dir = output_path / "valid"
    dead_letter_dir = output_path / "dead-letter"
    
    valid_dir.mkdir(exist_ok=True)
    dead_letter_dir.mkdir(exist_ok=True)
    
    return valid_dir, dead_letter_dir


def read_ndjson_lines(file_path: Path) -> Iterator[dict]:
    """
    Read NDJSON file line-by-line, yielding dicts.

    Args:
        file_path: Path to NDJSON file

    Returns:
        Iterator of dicts, one per valid JSON line

    Raises:
        None - skips empty files silently, malformed lines become None
    """
    if file_path.stat().st_size == 0:
        return
    
    with file_path.open('r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
