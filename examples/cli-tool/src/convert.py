# generated_from: behaviors/convert
# spec_hash: a619723338ad563e8faf40a9ccc9b099a7b8e3b14de16347730c5dcc1c2736c3
# generated_at: 2026-03-15T02:28:22.994832+00:00
# agent: implementation-agent
import csv
import json
import os
import re
from typing import Any

def convert(input_path: str, output_path: str | None, detect_types: bool, compact: bool) -> str:
    """
    Convert CSV file to JSON format.

    Args:
        input_path: Path to input CSV file
        output_path: Path to output JSON file, or None to return string only
        detect_types: Whether to detect and convert types (int/float/bool/null)
        compact: Whether to output compact JSON (no indentation)

    Returns:
        JSON string of the converted data

    Raises:
        FileNotFoundError: If input file does not exist
        ValueError: If file is empty, malformed CSV, duplicate columns, or too large
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No such file: {input_path}")

    file_size = os.path.getsize(input_path)
    if file_size == 0:
        raise ValueError("empty file")

    if file_size > 100 * 1024 * 1024:
        raise ValueError("file too large")

    rows = []
    column_names = []
    seen_columns = set()

    with open(input_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        row_num = 0
        try:
            for row in reader:
                row_num += 1
                if row_num == 1:
                    # Header row
                    for col in row:
                        col_lower = col.lower()
                        if col_lower in seen_columns:
                            raise ValueError(f"duplicate column: {col}")
                        seen_columns.add(col_lower)
                        column_names.append(col)
                    if not column_names:
                        raise ValueError("empty file")
                else:
                    # Data row
                    if len(row) != len(column_names):
                        raise ValueError(f"row {row_num} has wrong number of columns")
                    row_dict = {}
                    for i, value in enumerate(row):
                        if detect_types:
                            row_dict[column_names[i]] = detect_type(value)
                        else:
                            row_dict[column_names[i]] = value
                    rows.append(row_dict)
        except csv.Error as e:
            raise ValueError(f"malformed CSV at row {row_num}: {e}") from e

    json_data = json.dumps(rows, indent=2 if not compact else None, separators=(',', ':') if compact else None)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_data)

    return json_data

def detect_type(value: str) -> Any:
    value = value.strip()
    if not value:
        return None

    # Boolean detection (case-insensitive)
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False

    # Integer detection
    if re.match(r'^-?\d+$', value):
        return int(value)

    # Float detection
    if re.match(r'^-?\d+\.\d+$', value):
        return float(value)

    # String (everything else)
    return value
