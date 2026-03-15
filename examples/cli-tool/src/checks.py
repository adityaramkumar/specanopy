# generated_from: behaviors/validate
# spec_hash: 4b630e11f5156a31257969fa4f6b1943f1222426bf4a0aa5b4e943258389f73b
# generated_at: 2026-03-15T02:28:03.878047+00:00
# agent: implementation-agent
from pathlib import Path
from typing import NamedTuple


class CheckResult(NamedTuple):
    """Result of a single validation check."""
    is_valid: bool
    message: str


def check_file_exists_and_readable(file_path: str) -> CheckResult:
    """
    Check if file exists and is readable.

    Args:
        file_path: Path to the file

    Returns:
        CheckResult: (True, "") if valid, (False, error_message) if invalid

    Raises:
        None
    """
    path = Path(file_path)
    if not path.exists():
        return CheckResult(False, "file does not exist")
    if not path.is_file():
        return CheckResult(False, "not a file")
    try:
        path.stat()
        path.read_bytes()  # Test readability
        return CheckResult(True, "")
    except (OSError, PermissionError) as e:
        return CheckResult(False, f"not readable: {str(e)}")


def check_file_not_empty(file_path: str) -> CheckResult:
    """
    Check if file is not empty (0 bytes).

    Args:
        file_path: Path to the file

    Returns:
        CheckResult: (True, "") if valid, (False, "empty file") if invalid

    Raises:
        None
    """
    path = Path(file_path)
    if path.stat().st_size == 0:
        return CheckResult(False, "empty file")
    return CheckResult(True, "")


def check_file_size(file_path: str, max_size_mb: int = 100) -> CheckResult:
    """
    Check if file size does not exceed max_size_mb (default 100 MB).

    Args:
        file_path: Path to the file
        max_size_mb: Maximum allowed size in MB

    Returns:
        CheckResult: (True, "") if valid, (False, "file too large") if invalid

    Raises:
        None
    """
    path = Path(file_path)
    max_bytes = max_size_mb * 1024 * 1024
    if path.stat().st_size > max_bytes:
        return CheckResult(False, "file too large")
    return CheckResult(True, "")


def check_header_row(file_path: str) -> CheckResult:
    """
    Check if header row is present and parseable as CSV.

    Args:
        file_path: Path to the file

    Returns:
        CheckResult: (True, "") if valid, (False, error_message) if invalid

    Raises:
        None
    """
    import csv
    from .validate import get_header_row

    try:
        header = get_header_row(file_path)
        if not header:
            return CheckResult(False, "no header row")
        return CheckResult(True, "")
    except ValueError as e:
        return CheckResult(False, str(e))


def check_unique_columns(header_row: list[str]) -> CheckResult:
    """
    Check if column names in header are unique (case-insensitive).

    Args:
        header_row: List of column names from header row

    Returns:
        CheckResult: (True, "") if unique, (False, "duplicate column: {name}") if duplicate found

    Raises:
        None
    """
    lower_to_original = {}
    for col in header_row:
        lower = col.lower()
        if lower in lower_to_original:
            return CheckResult(False, f"duplicate column: {col}")
        lower_to_original[lower] = col
    return CheckResult(True, "")
