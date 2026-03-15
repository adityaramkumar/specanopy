# generated_from: contracts/formats/csv
# spec_hash: edb57b7d78a4502607e88d8c38e89699af9eb47e08d69b23dc093375f008231c
# generated_at: 2026-03-15T02:27:22.100859+00:00
# agent: testing-agent
# test_csv_validator.py
import pytest
import os
from csv_validator import validate_csv, is_valid_csv_structure

@pytest.fixture
def tmp_csv_file(tmp_path):
    return tmp_path / "test.csv"

class TestValidateCsv:
    def test_valid_csv_with_data(self, tmp_csv_file):
        content = 'name,age,city\nAlice,30,New York\nBob,25,Los Angeles'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        result = validate_csv(str(tmp_csv_file))
        assert len(result) == 2
        assert result[0] == {'name': 'Alice', 'age': '30', 'city': 'New York'}
        assert result[1] == {'name': 'Bob', 'age': '25', 'city': 'Los Angeles'}

    def test_valid_csv_only_header(self, tmp_csv_file):
        content = 'name,age,city'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        result = validate_csv(str(tmp_csv_file))
        assert len(result) == 0

    def test_empty_file_raises_value_error(self, tmp_csv_file):
        tmp_csv_file.write_bytes(b'')
        with pytest.raises(ValueError, match="empty file"):
            validate_csv(str(tmp_csv_file))

    def test_file_too_large_raises_value_error(self, tmp_csv_file):
        content = b'a' * (100 * 1024 * 1024 + 1)  # 100MB + 1 byte
        tmp_csv_file.write_bytes(content)
        with pytest.raises(ValueError, match="file too large"):
            validate_csv(str(tmp_csv_file))

    def test_duplicate_column_names_raises_value_error(self, tmp_csv_file):
        content = 'name,name,city\nAlice,30,New York'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        with pytest.raises(ValueError, match="duplicate column: name"):
            validate_csv(str(tmp_csv_file))

    def test_case_insensitive_duplicate_columns_raises_value_error(self, tmp_csv_file):
        content = 'Name,name,city\nAlice,30,New York'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        with pytest.raises(ValueError, match="duplicate column: name"):
            validate_csv(str(tmp_csv_file))

    def test_quoted_field_with_comma(self, tmp_csv_file):
        content = 'name,info\nAlice,"New York, NY"'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        result = validate_csv(str(tmp_csv_file))
        assert result[0]['info'] == 'New York, NY'

    def test_quoted_field_with_double_quotes(self, tmp_csv_file):
        content = 'name,quote\nAlice,"He said \"hello\""'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        result = validate_csv(str(tmp_csv_file))
        assert result[0]['quote'] == 'He said "hello"'

    def test_utf8_encoded_file(self, tmp_csv_file):
        content = 'name,city\nJosé,Madrid'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        result = validate_csv(str(tmp_csv_file))
        assert result[0]['name'] == 'José'

class TestIsValidCsvStructure:
    def test_valid_csv_with_data_returns_true(self, tmp_csv_file):
        content = 'name,age,city\nAlice,30,New York'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        assert is_valid_csv_structure(str(tmp_csv_file)) is True

    def test_valid_csv_only_header_returns_true(self, tmp_csv_file):
        content = 'name,age,city'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        assert is_valid_csv_structure(str(tmp_csv_file)) is True

    def test_empty_file_raises_value_error(self, tmp_csv_file):
        tmp_csv_file.write_bytes(b'')
        with pytest.raises(ValueError, match="empty file"):
            is_valid_csv_structure(str(tmp_csv_file))

    def test_file_too_large_raises_value_error(self, tmp_csv_file):
        content = b'a' * (100 * 1024 * 1024 + 1)
        tmp_csv_file.write_bytes(content)
        with pytest.raises(ValueError, match="file too large"):
            is_valid_csv_structure(str(tmp_csv_file))

    def test_duplicate_column_names_raises_value_error(self, tmp_csv_file):
        content = 'name,name,city\nAlice,30,New York'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        with pytest.raises(ValueError, match="duplicate column: name"):
            is_valid_csv_structure(str(tmp_csv_file))

    def test_case_insensitive_duplicate_columns_raises_value_error(self, tmp_csv_file):
        content = 'Name,name,city\nAlice,30,New York'
        tmp_csv_file.write_bytes(content.encode('utf-8'))
        with pytest.raises(ValueError, match="duplicate column: name"):
            is_valid_csv_structure(str(tmp_csv_file))
