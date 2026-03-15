# generated_from: contracts/formats/csv
# spec_hash: edb57b7d78a4502607e88d8c38e89699af9eb47e08d69b23dc093375f008231c
# generated_at: 2026-03-15T02:27:22.096364+00:00
# agent: implementation-agent
from typing import List, Dict, Any
import os


def validate_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Validates a CSV file against the contract specification and returns the parsed data.

    Args:
        file_path: Path to the CSV file

    Returns:
        List of dictionaries representing CSV rows, with header names as keys

    Raises:
        ValueError: "empty file" if file is 0 bytes
        ValueError: "file too large" if file exceeds 100 MB
        ValueError: "duplicate column: {name}" if column names are not unique (case-insensitive)
    """
    check_file_basics(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    rows = parse_csv(content)
    headers = rows[0] if rows else []
    check_duplicate_headers(headers)
    result = []
    for row in rows[1:]:
        row_dict = {h.lower(): v for h, v in zip(headers, row)}
        result.append({h: row_dict.get(h.lower(), '') for h in headers})
    return result


def is_valid_csv_structure(file_path: str) -> bool:
    """
    Checks if CSV file has valid structure without returning data.

    Args:
        file_path: Path to the CSV file

    Returns:
        True if file is valid, False otherwise

    Raises:
        ValueError: "empty file" if file is 0 bytes
        ValueError: "file too large" if file exceeds 100 MB
        ValueError: "duplicate column: {name}" if column names are not unique (case-insensitive)
    """
    check_file_basics(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    rows = parse_csv(content)
    if not rows:
        return False
    headers = rows[0]
    check_duplicate_headers(headers)
    return True


def check_file_basics(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise ValueError("empty file")
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise ValueError("empty file")
    if file_size > 100 * 1024 * 1024:
        raise ValueError("file too large")


def parse_csv(content: str) -> List[List[str]]:
    lines = content.strip().split('\n')
    if not lines:
        return []
    rows = []
    for line in lines:
        row = []
        i = 0
        while i < len(line):
            if line[i] == '"':
                # Parse quoted field
                field = []
                i += 1
                while i < len(line):
                    if line[i] == '"' and i + 1 < len(line) and line[i + 1] == '"':
                        field.append('"')
                        i += 2
                    elif line[i] == '"':
                        i += 1
                        break
                    else:
                        field.append(line[i])
                        i += 1
                row.append(''.join(field))
            else:
                # Parse unquoted field
                end = line.find(',', i)
                if end == -1:
                    end = len(line)
                field = line[i:end].strip()
                row.append(field)
                i = end + 1
        rows.append(row)
    return rows


def check_duplicate_headers(headers: List[str]) -> None:
    lower_headers = [h.lower() for h in headers]
    seen = set()
    for i, header in enumerate(lower_headers):
        if header in seen:
            raise ValueError(f"duplicate column: {headers[i]}")
        seen.add(header)
