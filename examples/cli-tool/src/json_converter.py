# generated_from: contracts/formats/json
# spec_hash: 8f053498a5673becd45aa5ef6eba1727bdeb891c42ec72c0e8ba055b6b13b7b2
# generated_at: 2026-03-15T02:27:44.642152+00:00
# agent: implementation-agent
from typing import List, Dict, Any, Iterator
import csv
import json
from pathlib import Path

from type_detector import TypeDetector
from output_formatter import OutputFormatter


class JsonConverter:
    def __init__(self, detect_types: bool = False, compact: bool = False):
        """
        Initialize the JSON converter.

        :param detect_types: Enable automatic type detection for fields
        :param compact: Use compact JSON output without indentation
        """
        self.detect_types = detect_types
        self.compact = compact
        self.type_detector = TypeDetector()
        self.formatter = OutputFormatter(compact)

    def convert(self, file_path: str) -> Iterator[str]:
        """
        Convert CSV file to JSON lines stream.

        :param file_path: Path to the input CSV file
        :raises FileNotFoundError: If the CSV file does not exist
        :raises PermissionError: If the file cannot be read
        :raises ValueError: If the CSV file has invalid format (no header, empty file)
        :return: Iterator yielding JSON lines as strings
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        try:
            with path.open('r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    raise ValueError("CSV file has no header or is empty")
                
                for row in reader:
                    if self.detect_types:
                        row = self.type_detector.detect_row(row)
                    yield self.formatter.dumps(row)
        except PermissionError as e:
            raise PermissionError(f"Cannot read file {file_path}: {e}") from e

    def convert_all(self, file_path: str) -> str:
        """
        Convert entire CSV file to single JSON array string.

        :param file_path: Path to the input CSV file
        :raises FileNotFoundError: If the CSV file does not exist
        :raises PermissionError: If the file cannot be read
        :raises ValueError: If the CSV file has invalid format (no header, empty file)
        :return: Complete JSON array as UTF-8 encoded string
        """
        rows = self.rows(file_path)
        return self.formatter.format_rows(rows)

    def rows(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse CSV and return rows as list of dictionaries with type detection applied.

        :param file_path: Path to the input CSV file
        :raises FileNotFoundError: If the CSV file does not exist
        :raises PermissionError: If the file cannot be read
        :raises ValueError: If the CSV file has invalid format
        :return: List of row dictionaries with detected types
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        try:
            with path.open('r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    raise ValueError("CSV file has no header or is empty")
                
                rows = []
                for row in reader:
                    if self.detect_types:
                        row = self.type_detector.detect_row(row)
                    rows.append(row)
                return rows
        except PermissionError as e:
            raise PermissionError(f"Cannot read file {file_path}: {e}") from e
