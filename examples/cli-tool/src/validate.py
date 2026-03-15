# generated_from: behaviors/validate
# spec_hash: 4b630e11f5156a31257969fa4f6b1943f1222426bf4a0aa5b4e943258389f73b
# generated_at: 2026-03-15T02:28:03.864995+00:00
# agent: implementation-agent
def validate(input_path: str) -> tuple[bool, str]:
    """
    Validate CSV file according to specification.

    Performs checks in order:
    1. File exists and is readable
    2. File is not empty (0 bytes)
    3. File size does not exceed 100 MB
    4. Header row is present and parseable
    5. Column names are unique (case-insensitive)

    Returns:
        tuple[bool, str]: (True, summary_message) if valid, (False, error_message) if invalid

    Raises:
        None - all errors handled internally and returned as (False, message)
    """
    from .checks import (
        check_file_exists_and_readable,
        check_file_not_empty,
        check_file_size,
        check_header_row,
        check_unique_columns,
        CheckResult,
    )

    checks = [
        check_file_exists_and_readable,
        check_file_not_empty,
        check_file_size,
        check_header_row,
        lambda path: check_unique_columns(get_header_row(path)),
    ]

    for check in checks:
        result: CheckResult = check(input_path)
        if not result.is_valid:
            return False, result.message

    # All checks passed, count rows and columns
    header_row = get_header_row(input_path)
    num_columns = len(header_row)
    num_rows = count_csv_rows(input_path)

    return True, f"Valid: {num_rows} rows, {num_columns} columns"


def get_header_row(file_path: str) -> list[str]:
    """Extract header row from CSV file."""
    import csv
    from pathlib import Path

    path = Path(file_path)
    with path.open('r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            return next(reader)
        except StopIteration:
            raise ValueError("no header row")
        except csv.Error as e:
            raise ValueError(f"invalid header: {str(e)}")


def count_csv_rows(file_path: str) -> int:
    """Count total rows in CSV file (including header)."""
    import csv
    from pathlib import Path

    path = Path(file_path)
    with path.open('r', encoding='utf-8') as f:
        return sum(1 for _ in csv.reader(f))
