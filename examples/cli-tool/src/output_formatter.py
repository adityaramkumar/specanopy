# generated_from: contracts/formats/json
# spec_hash: 8f053498a5673becd45aa5ef6eba1727bdeb891c42ec72c0e8ba055b6b13b7b2
# generated_at: 2026-03-15T02:27:44.660862+00:00
# agent: implementation-agent
import json
from typing import Iterator, List, Dict, Any


class OutputFormatter:
    def __init__(self, compact: bool = False):
        """
        Initialize output formatter.

        :param compact: Use compact JSON (no indentation) if True
        """
        self.compact = compact
        self.indent = None if compact else 2

    def format_rows(self, rows: List[Dict[str, Any]]) -> str:
        """
        Format list of rows as complete JSON array.

        :param rows: List of row dictionaries
        :return: Pretty-printed or compact JSON array string (UTF-8)
        """
        return self.dumps(rows)

    def format_row_stream(self, rows: Iterator[Dict[str, Any]]) -> Iterator[str]:
        """
        Format rows as streaming JSON lines.

        :param rows: Iterator of row dictionaries
        :return: Iterator of JSON lines (one object per line)
        """
        for row in rows:
            yield self.dumps(row)

    def dumps(self, obj: Any) -> str:
        """
        Serialize Python object to JSON string with current formatting options.

        :param obj: Python object to serialize
        :return: JSON string (pretty-printed or compact)
        :raises TypeError: If object cannot be serialized to JSON
        """
        return json.dumps(obj, indent=self.indent, ensure_ascii=False)
