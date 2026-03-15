# generated_from: contracts/formats/json
# spec_hash: 8f053498a5673becd45aa5ef6eba1727bdeb891c42ec72c0e8ba055b6b13b7b2
# generated_at: 2026-03-15T02:27:44.645989+00:00
# agent: implementation-agent
from typing import Dict, Any
import re


class TypeDetector:
    INTEGER_PATTERN = re.compile(r'^-?\d+$')
    FLOAT_PATTERN = re.compile(r'^-?\d+\.\d+$')

    @staticmethod
    def detect(value: str) -> Any:
        """
        Detect and convert string value to appropriate JSON type.

        Type detection rules:
        - Integers: ^-?\d+$
        - Floats: ^-?\d+\.\d+$
        - Booleans: true/false (case-insensitive)
        - Null: empty string
        - Everything else: string

        :param value: Input string value from CSV field
        :return: Detected Python type (str, int, float, bool, None)
        """
        if not value:  # empty string
            return None
        
        value_lower = value.lower().strip()
        if value_lower == 'true':
            return True
        elif value_lower == 'false':
            return False
        
        if TypeDetector.INTEGER_PATTERN.match(value):
            return int(value)
        elif TypeDetector.FLOAT_PATTERN.match(value):
            return float(value)
        
        return value

    @staticmethod
    def detect_row(row: Dict[str, str]) -> Dict[str, Any]:
        """
        Apply type detection to all values in a row dictionary.

        :param row: Dictionary with string values from CSV row
        :return: Dictionary with detected types applied to values
        """
        return {key: TypeDetector.detect(value) for key, value in row.items()}
