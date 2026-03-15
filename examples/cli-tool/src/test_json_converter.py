# generated_from: contracts/formats/json
# spec_hash: 8f053498a5673becd45aa5ef6eba1727bdeb891c42ec72c0e8ba055b6b13b7b2
# generated_at: 2026-03-15T02:27:44.664296+00:00
# agent: testing-agent
import pytest
import tempfile
import os
from json_converter import JsonConverter


@pytest.fixture
def sample_csv(tmp_path):
    """Create sample CSV file for testing."""
    csv_content = '''name,age,active,price,notes\nAlice,30,true,19.99,\nBob,25,false,0.0,has notes\n'''
    csv_path = tmp_path / 'test.csv'
    csv_path.write_text(csv_content, encoding='utf-8')
    return str(csv_path)


@pytest.fixture
def empty_csv(tmp_path):
    """Create empty CSV file."""
    csv_path = tmp_path / 'empty.csv'
    csv_path.write_text('', encoding='utf-8')
    return str(csv_path)


@pytest.fixture
def no_header_csv(tmp_path):
    """Create CSV without header."""
    csv_content = 'Alice,30,true\nBob,25,false\n'
    csv_path = tmp_path / 'noheader.csv'
    csv_path.write_text(csv_content, encoding='utf-8')
    return str(csv_path)


class TestJsonConverter:
    def test_rows_default_types(self, sample_csv):
        """Verify rows parsed as strings by default (no type detection)."""
        converter = JsonConverter(detect_types=False)
        rows = converter.rows(sample_csv)
        assert len(rows) == 2
        assert rows[0] == {
            'name': 'Alice',
            'age': '30',
            'active': 'true',
            'price': '19.99',
            'notes': ''
        }
        # All values are strings
        for row in rows:
            for value in row.values():
                assert isinstance(value, str)

    def test_rows_with_type_detection(self, sample_csv):
        """Verify type detection converts values appropriately."""
        converter = JsonConverter(detect_types=True)
        rows = converter.rows(sample_csv)
        assert len(rows) == 2
        assert rows[0] == {
            'name': 'Alice',
            'age': 30,
            'active': True,
            'price': 19.99,
            'notes': None
        }

    def test_convert_all_pretty_default(self, sample_csv):
        """Verify complete JSON array pretty-printed with 2-space indentation."""
        converter = JsonConverter(detect_types=True, compact=False)
        result = converter.convert_all(sample_csv)
        import json
        parsed = json.loads(result)
        assert isinstance(parsed, list)
        assert len(parsed) == 2
        assert '  ' in result  # Pretty printed
        assert isinstance(parsed[0]['age'], int)
        assert parsed[0]['active'] is True

    def test_convert_all_compact(self, sample_csv):
        """Verify compact JSON output without indentation."""
        converter = JsonConverter(detect_types=True, compact=True)
        result = converter.convert_all(sample_csv)
        import json
        parsed = json.loads(result)
        assert len(parsed) == 2
        assert '\n' not in result[1:-1]  # Compact

    def test_convert_stream(self, sample_csv):
        """Verify streaming JSON lines iterator."""
        converter = JsonConverter(detect_types=True)
        lines = list(converter.convert(sample_csv))
        assert len(lines) == 2
        import json
        for line in lines:
            assert line.endswith('\n')
            obj = json.loads(line.strip())
            assert isinstance(obj, dict)

    def test_raises_filenotfounderror(self, tmp_path):
        """Verify FileNotFoundError for missing file."""
        converter = JsonConverter()
        with pytest.raises(FileNotFoundError):
            converter.rows('/nonexistent.csv')

    def test_raises_permissionerror_protected_file(self, tmp_path):
        """Verify PermissionError for unreadable file."""
        protected_file = tmp_path / 'protected.csv'
        protected_file.write_text('test')
        protected_file.chmod(0o000)  # Remove read permissions
        converter = JsonConverter()
        with pytest.raises(PermissionError):
            converter.rows(str(protected_file))

    def test_raises_valueerror_empty_file(self, empty_csv):
        """Verify ValueError for empty CSV file."""
        converter = JsonConverter()
        with pytest.raises(ValueError, match='empty file'):
            converter.rows(empty_csv)

    def test_raises_valueerror_no_header(self, no_header_csv):
        """Verify ValueError for CSV without header."""
        converter = JsonConverter()
        with pytest.raises(ValueError, match='no header'):
            converter.rows(no_header_csv)
