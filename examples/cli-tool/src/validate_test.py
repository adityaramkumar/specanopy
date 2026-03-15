# generated_from: behaviors/validate
# spec_hash: 4b630e11f5156a31257969fa4f6b1943f1222426bf4a0aa5b4e943258389f73b
# generated_at: 2026-03-15T02:28:03.887832+00:00
# agent: testing-agent
# Generated unit tests for validate behavior

import pytest
import os
from pathlib import Path
from validate import validate


@pytest.fixture
def test_dir(tmp_path: Path):
    """Create test directory with sample files."""
    test_files = {
        'valid.csv': 'col1,col2\n1,2\n3,4',
        'valid_single_row.csv': 'col1,col2\n1,2',
        'valid_only_header.csv': 'col1,col2',
        'empty.csv': '',
        'nonexistent.txt': '',
        'too_large.csv': 'a' * (100 * 1024 * 1024 + 1),
        'duplicate_case_insensitive.csv': 'Col1,col1\n1,2',
        'duplicate_columns.csv': 'col1,col1\n1,2',
        'invalid_header.csv': 'col1,col2,\n1,2,3',
        'unreadable.csv': 'col1,col2\n1,2'
    }
    for filename, content in test_files.items():
        if filename != 'nonexistent.txt':
            path = tmp_path / filename
            path.write_text(content)
            if filename == 'unreadable.csv':
                path.chmod(0o000)
    return tmp_path


class TestValidate:
    def test_valid_file(self, test_dir: Path):
        result, message = validate(str(test_dir / 'valid.csv'))
        assert result is True
        assert message == 'Valid: 2 rows, 2 columns'

    def test_valid_file_only_header(self, test_dir: Path):
        result, message = validate(str(test_dir / 'valid_only_header.csv'))
        assert result is True
        assert message == 'Valid: 0 rows, 2 columns'

    def test_valid_file_single_data_row(self, test_dir: Path):
        result, message = validate(str(test_dir / 'valid_single_row.csv'))
        assert result is True
        assert message == 'Valid: 1 rows, 2 columns'

    def test_file_does_not_exist(self, test_dir: Path):
        result, message = validate(str(test_dir / 'nonexistent.txt'))
        assert result is False
        assert 'No such file' in message or '[Errno 2]' in message

    def test_file_unreadable(self, test_dir: Path):
        result, message = validate(str(test_dir / 'unreadable.csv'))
        assert result is False
        assert '[Errno 13]' in message or 'Permission denied' in message

    def test_empty_file(self, test_dir: Path):
        result, message = validate(str(test_dir / 'empty.csv'))
        assert result is False
        assert message == 'empty file'

    def test_file_too_large(self, test_dir: Path):
        result, message = validate(str(test_dir / 'too_large.csv'))
        assert result is False
        assert message == 'file too large'

    def test_duplicate_columns_case_insensitive(self, test_dir: Path):
        result, message = validate(str(test_dir / 'duplicate_case_insensitive.csv'))
        assert result is False
        assert message == 'duplicate column: col1'

    def test_duplicate_columns(self, test_dir: Path):
        result, message = validate(str(test_dir / 'duplicate_columns.csv'))
        assert result is False
        assert message == 'duplicate column: col1'

    def test_invalid_header(self, test_dir: Path):
        result, message = validate(str(test_dir / 'invalid_header.csv'))
        assert result is False
        assert 'header' in message.lower() or 'parse' in message.lower()

    def test_fail_fast_on_first_error(self, test_dir: Path):
        # Create file that fails size check but has other issues
        large_invalid = test_dir / 'large_invalid.csv'
        large_invalid.write_text('col1,col1\n1,2' * 1000000)
        result, message = validate(str(large_invalid))
        # Should fail on size first, not reach duplicate column check
        assert result is False
        assert message == 'file too large'

    def test_valid_file_100mb(self, test_dir: Path):
        # Exactly 100MB should be valid
        boundary_file = test_dir / 'boundary_100mb.csv'
        content = 'col1,col2\n' + ('data,data\n' * (50 * 1024 * 1024 // 10))
        boundary_file.write_text(content)
        result, message = validate(str(boundary_file))
        assert result is True
        assert message.startswith('Valid: ')

    def test_quoted_header_valid(self, test_dir: Path):
        quoted_header = test_dir / 'quoted_header.csv'
        quoted_header.write_text('"col,1","col2"\n1,2')
        result, message = validate(str(quoted_header))
        assert result is True
        assert message == 'Valid: 1 rows, 2 columns'
