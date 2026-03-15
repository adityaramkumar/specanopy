# generated_from: behaviors/validate
# spec_hash: 4b630e11f5156a31257969fa4f6b1943f1222426bf4a0aa5b4e943258389f73b
# generated_at: 2026-03-15T02:28:03.888195+00:00
# agent: testing-agent
# Generated unit tests for individual validation checks

import pytest
from pathlib import Path
from checks import (
    CheckResult,
    check_file_exists_and_readable,
    check_file_not_empty,
    check_file_size,
    check_header_row,
    check_unique_columns
)


@pytest.fixture
def test_files(tmp_path: Path):
    test_files = {
        'exists_readable.txt': 'content',
        'empty.txt': '',
        'small.csv': 'header\n1,2',
        'large.csv': 'a' * (101 * 1024 * 1024),
        'valid_header.csv': 'col1,col2',
        'invalid_header.csv': 'unparseable',
    }
    for name, content in test_files.items():
        (tmp_path / name).write_text(content)
    return tmp_path


class TestCheckFileExistsAndReadable:
    def test_exists_and_readable(self, test_files: Path):
        result = check_file_exists_and_readable(str(test_files / 'exists_readable.txt'))
        assert result == CheckResult(True, '')

    def test_nonexistent(self, test_files: Path):
        result = check_file_exists_and_readable(str(test_files / 'missing.txt'))
        assert result.is_valid is False
        assert result.message != ''

    def test_unreadable(self, test_files: Path):
        unreadable = test_files / 'unreadable.txt'
        unreadable.write_text('content')
        unreadable.chmod(0o000)
        result = check_file_exists_and_readable(str(unreadable))
        assert result.is_valid is False
        assert result.message != ''


class TestCheckFileNotEmpty:
    def test_not_empty(self, test_files: Path):
        result = check_file_not_empty(str(test_files / 'exists_readable.txt'))
        assert result == CheckResult(True, '')

    def test_empty_file(self, test_files: Path):
        result = check_file_not_empty(str(test_files / 'empty.txt'))
        assert result == CheckResult(False, 'empty file')


class TestCheckFileSize:
    def test_small_file(self, test_files: Path):
        result = check_file_size(str(test_files / 'small.csv'))
        assert result == CheckResult(True, '')

    def test_large_file(self, test_files: Path):
        result = check_file_size(str(test_files / 'large.csv'))
        assert result == CheckResult(False, 'file too large')

    def test_custom_max_size(self):
        small_file = Path('small.txt')
        small_file.write_text('a' * (50 * 1024 * 1024))
        result = check_file_size(str(small_file), max_size_mb=40)
        assert result.is_valid is False
        assert result.message == 'file too large'


class TestCheckHeaderRow:
    def test_valid_header(self, test_files: Path):
        result = check_header_row(str(test_files / 'valid_header.csv'))
        assert result == CheckResult(True, '')

    def test_invalid_header(self, test_files: Path):
        result = check_header_row(str(test_files / 'invalid_header.csv'))
        assert result.is_valid is False
        assert result.message != ''

    def test_quoted_header_valid(self, test_files: Path):
        quoted = test_files / 'quoted.csv'
        quoted.write_text('"col,1","col2"')
        result = check_header_row(str(quoted))
        assert result == CheckResult(True, '')


class TestCheckUniqueColumns:
    def test_unique_columns(self):
        result = check_unique_columns(['col1', 'col2', 'col3'])
        assert result == CheckResult(True, '')

    def test_duplicate_case_insensitive(self):
        result = check_unique_columns(['Col1', 'col1', 'col2'])
        assert result.is_valid is False
        assert result.message == 'duplicate column: col1'

    def test_duplicate_columns(self):
        result = check_unique_columns(['col1', 'col1', 'col2'])
        assert result.is_valid is False
        assert result.message == 'duplicate column: col1'

    def test_empty_header(self):
        result = check_unique_columns([])
        assert result == CheckResult(True, '')

    def test_single_column(self):
        result = check_unique_columns(['col1'])
        assert result == CheckResult(True, '')
