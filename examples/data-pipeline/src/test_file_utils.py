# generated_from: behaviors/ingest
# spec_hash: a46bf4c24197a3b855328de74eab6c7676c144c326dc88fd066bc5484a1f8221
# generated_at: 2026-03-15T02:32:11.596749+00:00
# agent: implementation-agent
import pytest
import tempfile
import os
from pathlib import Path
from file_utils import scan_ndjson_files, create_output_dirs, read_ndjson_lines

class TestFileUtils:
    def test_scan_ndjson_files_found(self, tmp_path):
        # Create input dir with ndjson files
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        
        (input_dir / "file1.ndjson").write_text('{"test": 1}\n')
        (input_dir / "file2.ndjson").write_text('{"test": 2}\n')
        
        files = scan_ndjson_files(str(input_dir))
        assert len(files) == 2

    def test_scan_ndjson_files_not_found(self):
        with pytest.raises(FileNotFoundError):
            scan_ndjson_files("/nonexistent/dir")

    def test_scan_ndjson_files_no_ndjson(self, tmp_path):
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        (input_dir / "file.txt").write_text("text")
        
        with pytest.raises(ValueError, match="no .ndjson files found"):
            scan_ndjson_files(str(input_dir))

    def test_scan_ndjson_files_empty_skipped(self, tmp_path):
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        
        empty_file = input_dir / "empty.ndjson"
        empty_file.write_text("")
        
        (input_dir / "valid.ndjson").write_text('{"test": 1}\n')
        
        files = scan_ndjson_files(str(input_dir))
        assert len(files) == 1
        assert empty_file not in files

    def test_create_output_dirs(self, tmp_path):
        output_dir = tmp_path / "output"
        
        valid_dir, dead_letter_dir = create_output_dirs(str(output_dir))
        
        assert valid_dir.exists()
        assert dead_letter_dir.exists()
        assert (valid_dir / "..").samefile(output_dir)
        assert (dead_letter_dir / "..").samefile(output_dir)

    def test_read_ndjson_lines_valid(self, tmp_path):
        file_path = tmp_path / "test.ndjson"
        file_path.write_text('{"a": 1}\n{"b": 2}\n{"c": 3}\n')
        
        events = list(read_ndjson_lines(file_path))
        assert len(events) == 3
        assert events[0] == {"a": 1}
        assert events[1] == {"b": 2}
        assert events[2] == {"c": 3}

    def test_read_ndjson_lines_malformed_skipped(self, tmp_path):
        file_path = tmp_path / "test.ndjson"
        file_path.write_text('{"a": 1}\ninvalid json\n{"b": 2}\n')
        
        events = list(read_ndjson_lines(file_path))
        assert len(events) == 2
        assert events[0] == {"a": 1}
        assert events[1] == {"b": 2}

    def test_read_ndjson_lines_empty_skipped(self, tmp_path):
        file_path = tmp_path / "empty.ndjson"
        file_path.touch()
        
        events = list(read_ndjson_lines(file_path))
        assert len(events) == 0
