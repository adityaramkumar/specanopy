# generated_from: behaviors/convert
# spec_hash: a619723338ad563e8faf40a9ccc9b099a7b8e3b14de16347730c5dcc1c2736c3
# generated_at: 2026-03-15T02:28:22.997423+00:00
# agent: testing-agent
# test_convert.py

import pytest
import os
import tempfile
from pathlib import Path

from convert import convert


@pytest.fixture
def create_csv_file(tmp_path: Path, content: str) -> Path:
    file_path = tmp_path / "test.csv"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def create_large_csv_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "large.csv"
    # Create file > 100MB
    file_path.write_bytes(b"header1,header2\n" + b"data,data\n" * 3_000_000)
    return str(file_path)


class TestHappyPath:
    def test_single_row_no_type_detection(self, create_csv_file):
        csv_content = "name,age,city\nAlice,30,New York"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=False, compact=False)
        
        expected = '[
  {
    "name": "Alice",
    "age": "30",
    "city": "New York"
  }
]'
        assert result == expected

    def test_single_row_with_type_detection(self, create_csv_file):
        csv_content = "name,age,city\nAlice,30,New York"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "name": "Alice",
    "age": 30,
    "city": "New York"
  }
]'
        assert result == expected

    def test_multiple_rows(self, create_csv_file):
        csv_content = "name,age,city\nsmith,25,LA\njones,35,Chicago"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=False, compact=False)
        
        expected = '[
  {
    "name": "smith",
    "age": "25",
    "city": "LA"
  },
  {
    "name": "jones",
    "age": "35",
    "city": "Chicago"
  }
]'
        assert result == expected

    def test_only_header_row(self, create_csv_file):
        csv_content = "name,age"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=False, compact=False)
        
        assert result == "[]"

    def test_write_to_output_file(self, create_csv_file, tmp_path: Path):
        csv_content = "name,age\nBob,40"
        input_path = create_csv_file(csv_content)
        output_path = tmp_path / "output.json"
        
        result = convert(str(input_path), str(output_path), detect_types=False, compact=False)
        
        assert os.path.exists(output_path)
        file_content = output_path.read_text(encoding="utf-8")
        assert result == file_content
        assert file_content == '[\n  {\n    "name": "Bob",\n    "age": "40"\n  }\n]'

    def test_compact_output(self, create_csv_file):
        csv_content = "name,age\nBob,40"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=False, compact=True)
        
        expected = '[{ "name": "Bob", "age": "40" }]'
        assert result == expected


class TestTypeDetection:
    def test_integer_detection(self, create_csv_file):
        csv_content = "id,name\n123,Alice"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "id": 123,
    "name": "Alice"
  }
]'
        assert result == expected

    def test_negative_integer(self, create_csv_file):
        csv_content = "balance\n-500"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "balance": -500
  }
]'
        assert result == expected

    def test_float_detection(self, create_csv_file):
        csv_content = "price\n12.99"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "price": 12.99
  }
]'
        assert result == expected

    def test_negative_float(self, create_csv_file):
        csv_content = "temp\n-3.14"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "temp": -3.14
  }
]'
        assert result == expected

    def test_boolean_detection_true(self, create_csv_file):
        csv_content = "active\ntrue"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "active": true
  }
]'
        assert result == expected

    def test_boolean_detection_false_case_insensitive(self, create_csv_file):
        csv_content = "active\nFALSE"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "active": false
  }
]'
        assert result == expected

    def test_null_detection_empty_field(self, create_csv_file):
        csv_content = "name,email\nAlice,"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "name": "Alice",
    "email": null
  }
]'
        assert result == expected

    def test_mixed_types(self, create_csv_file):
        csv_content = "id,name,price,active,notes\n1,Bob,19.99,true,test"
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=True, compact=False)
        
        expected = '[
  {
    "id": 1,
    "name": "Bob",
    "price": 19.99,
    "active": true,
    "notes": "test"
  }
]'
        assert result == expected


class TestQuotedFields:
    def test_quoted_field_with_comma(self, create_csv_file):
        csv_content = 'name,address\n"Smith, Jr.","123 Main St"'
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=False, compact=False)
        
        expected = '[
  {
    "name": "Smith, Jr.",
    "address": "123 Main St"
  }
]'
        assert result == expected

    def test_escaped_double_quotes(self, create_csv_file):
        csv_content = 'name,quote\nJohn,"He said ""hello"""'
        input_path = create_csv_file(csv_content)
        
        result = convert(input_path, None, detect_types=False, compact=False)
        
        expected = '[
  {
    "name": "John",
    "quote": "He said \"hello\"""
  }
]'
        assert result == expected


class TestErrorHandling:
    def test_file_not_found(self, tmp_path: Path):
        nonexistent_path = str(tmp_path / "nonexistent.csv")
        
        with pytest.raises(FileNotFoundError):
            convert(nonexistent_path, None, False, False)

    def test_empty_file(self, tmp_path: Path):
        empty_path = tmp_path / "empty.csv"
        empty_path.touch()
        
        with pytest.raises(ValueError, match="empty file"):
            convert(str(empty_path), None, False, False)

    def test_duplicate_columns_case_insensitive(self, create_csv_file):
        csv_content = "name,NAME,age\nAlice,30"
        input_path = create_csv_file(csv_content)
        
        with pytest.raises(ValueError, match="duplicate column: name"):
            convert(input_path, None, False, False)

    def test_file_too_large(self, create_large_csv_file):
        input_path = create_large_csv_file()
        
        with pytest.raises(ValueError, match="file too large"):
            convert(input_path, None, False, False)

    @pytest.mark.parametrize("malformed", [
        "header1,header2\ndata1",  # missing second field
        ",header2\nvalue1,data2",  # empty header
        "header1,,header3\ndata1,data2,data3",  # empty header field
    ])
    def test_malformed_csv(self, create_csv_file, malformed):
        input_path = create_csv_file(malformed)
        
        with pytest.raises(ValueError):
            convert(input_path, None, False, False)
