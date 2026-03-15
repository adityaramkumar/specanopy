# generated_from: contracts/formats/json
# spec_hash: 8f053498a5673becd45aa5ef6eba1727bdeb891c42ec72c0e8ba055b6b13b7b2
# generated_at: 2026-03-15T02:27:44.664153+00:00
# agent: testing-agent
import pytest
import json
from output_formatter import OutputFormatter


class TestOutputFormatter:
    def test_format_rows_pretty_default(self):
        """Verify pretty-printed JSON array with 2-space indentation (default)."""
        formatter = OutputFormatter(compact=False)
        rows = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25}
        ]
        result = formatter.format_rows(rows)
        parsed = json.loads(result)
        assert parsed == rows
        assert '  ' in result  # Contains 2-space indentation
        assert result.startswith('[')
        assert result.endswith(']\n')

    def test_format_rows_compact(self):
        """Verify compact JSON array without indentation."""
        formatter = OutputFormatter(compact=True)
        rows = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25}
        ]
        result = formatter.format_rows(rows)
        parsed = json.loads(result)
        assert parsed == rows
        assert '\n' not in result[1:-1]  # No newlines between objects
        assert result == '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'

    def test_format_row_stream(self):
        """Verify streaming JSON lines (one object per line)."""
        formatter = OutputFormatter(compact=False)
        rows = iter([{'name': 'Alice'}, {'name': 'Bob'}])
        result = list(formatter.format_row_stream(rows))
        assert len(result) == 2
        assert json.loads(result[0]) == {'name': 'Alice'}
        assert json.loads(result[1]) == {'name': 'Bob'}
        for line in result:
            assert line.endswith('\n')

    def test_dumps_pretty(self):
        """Verify object serialization with pretty formatting."""
        formatter = OutputFormatter(compact=False)
        obj = {'key': 'value', 'num': 123}
        result = formatter.dumps(obj)
        parsed = json.loads(result)
        assert parsed == obj
        assert '  ' in result

    def test_dumps_compact(self):
        """Verify object serialization with compact formatting."""
        formatter = OutputFormatter(compact=True)
        obj = {'key': 'value', 'num': 123}
        result = formatter.dumps(obj)
        assert result == '{"key":"value","num":123}'
        assert json.loads(result) == obj

    def test_dumps_raises_type_error(self):
        """Verify TypeError raised for non-serializable objects."""
        formatter = OutputFormatter()
        with pytest.raises(TypeError):
            formatter.dumps(set([1, 2, 3]))
