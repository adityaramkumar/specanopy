# generated_from: behaviors/ingest
# spec_hash: a46bf4c24197a3b855328de74eab6c7676c144c326dc88fd066bc5484a1f8221
# generated_at: 2026-03-15T02:32:11.599730+00:00
# agent: testing-agent
# test_ingest.py
import pytest
import tempfile
import shutil
import os
from pathlib import Path
from ingest import ingest

@pytest.fixture
def setup_dirs(tmp_path: Path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    return str(input_dir), str(output_dir)

class TestIngestHappyPath:
    def test_processes_valid_ndjson_files(self, setup_dirs):
        input_dir, output_dir = setup_dirs
        
        # Create valid NDJSON file
        ndjson_path = Path(input_dir) / "events.ndjson"
        valid_event = {
            "event_id": "123e4567-e89b-12d3-a456-426614174000",
            "event_type": "page_view",
            "timestamp": "2023-01-01T12:00:00Z",
            "user_id": "user-123",
            "properties": {"page": "home"},
            "source": "web"
        }
        ndjson_path.write_text(json.dumps(valid_event) + "\n")
        
        result = ingest(input_dir, output_dir)
        
        assert result == {"valid": 1, "invalid": 0, "files": 1}
        valid_file = Path(output_dir) / "valid" / "events.ndjson"
        assert valid_file.exists()
        assert valid_file.read_text().strip() == json.dumps(valid_event)
        
    def test_processes_mixed_valid_invalid_events(self, setup_dirs):
        input_dir, output_dir = setup_dirs
        
        ndjson_path = Path(input_dir) / "mixed.ndjson"
        valid_event = {
            "event_id": "123e4567-e89b-12d3-a456-426614174000",
            "event_type": "click",
            "timestamp": "2023-01-01T12:00:00Z",
            "properties": {"button": "submit"},
            "source": "web"
        }
        invalid_event = {
            "event_id": "invalid-uuid",
            "event_type": "invalid_type",
            "timestamp": "bad-timestamp",
            "properties": "not-a-dict",
            "source": "invalid_source"
        }
        ndjson_path.write_text(
            json.dumps(valid_event) + "\n" + json.dumps(invalid_event) + "\n"
        )
        
        result = ingest(input_dir, output_dir)
        
        assert result == {"valid": 1, "invalid": 1, "files": 1}
        valid_file = Path(output_dir) / "valid" / "events.ndjson"
        dead_letter_file = Path(output_dir) / "dead-letter" / "events.ndjson"
        
        assert valid_file.exists()
        assert dead_letter_file.exists()
        
    def test_counts_multiple_files_correctly(self, setup_dirs):
        input_dir, output_dir = setup_dirs
        
        # File 1: 2 valid
        file1 = Path(input_dir) / "file1.ndjson"
        valid1 = {
            "event_id": "1",
            "event_type": "page_view",
            "timestamp": "2023-01-01T12:00:00Z",
            "properties": {},
            "source": "web"
        }
        valid2 = {
            "event_id": "2",
            "event_type": "signup",
            "timestamp": "2023-01-01T12:00:00Z",
            "properties": {},
            "source": "api"
        }
        file1.write_text(json.dumps(valid1) + "\n" + json.dumps(valid2) + "\n")
        
        # File 2: 1 valid, 1 invalid
        file2 = Path(input_dir) / "file2.ndjson"
        file2.write_text(json.dumps(valid1) + "\n{" + "\n")
        
        result = ingest(input_dir, output_dir)
        
        assert result == {"valid": 3, "invalid": 1, "files": 2}

class TestIngestErrorHandling:
    def test_raises_filenotfounderror_for_missing_input_dir(self, tmp_path: Path):
        input_dir = str(tmp_path / "missing")
        output_dir = str(tmp_path / "output")
        
        with pytest.raises(FileNotFoundError):
            ingest(input_dir, output_dir)
    
    def test_raises_valueerror_for_no_ndjson_files(self, setup_dirs):
        input_dir, output_dir = setup_dirs
        
        # Create non-ndjson files
        (Path(input_dir) / "data.json").touch()
        (Path(input_dir) / "data.txt").touch()
        
        with pytest.raises(ValueError, match="no .ndjson files found"):
            ingest(input_dir, output_dir)
    
    def test_skips_empty_files_silently(self, setup_dirs):
        input_dir, output_dir = setup_dirs
        
        # Create empty NDJSON file
        (Path(input_dir) / "empty.ndjson").touch()
        
        result = ingest(input_dir, output_dir)
        
        assert result == {"valid": 0, "invalid": 0, "files": 1}

class TestIngestEdgeCases:
    def test_single_event_file(self, setup_dirs):
        input_dir, output_dir = setup_dirs
        
        ndjson_path = Path(input_dir) / "single.ndjson"
        event = {
            "event_id": "123e4567-e89b-12d3-a456-426614174000",
            "event_type": "purchase",
            "timestamp": "2023-01-01T12:00:00.000Z",
            "user_id": None,
            "properties": {},
            "source": "mobile"
        }
        ndjson_path.write_text(json.dumps(event) + "\n")
        
        result = ingest(input_dir, output_dir)
        
        assert result == {"valid": 1, "invalid": 0, "files": 1}
    
    def test_all_invalid_events(self, setup_dirs):
        input_dir, output_dir = setup_dirs
        
        ndjson_path = Path(input_dir) / "all-invalid.ndjson"
        invalid_event = {"missing_fields": True}
        ndjson_path.write_text(json.dumps(invalid_event) + "\n")
        
        result = ingest(input_dir, output_dir)
        
        assert result == {"valid": 0, "invalid": 1, "files": 1}
        dead_letter_file = Path(output_dir) / "dead-letter" / "events.ndjson"
        assert dead_letter_file.exists()
    
    def test_preserves_dead_letter_error_field(self, setup_dirs):
        input_dir, output_dir = setup_dirs
        
        ndjson_path = Path(input_dir) / "invalid.ndjson"
        invalid_event = {"event_id": "not-uuid"}
        ndjson_path.write_text(json.dumps(invalid_event) + "\n")
        
        result = ingest(input_dir, output_dir)
        
        dead_letter_file = Path(output_dir) / "dead-letter" / "events.ndjson"
        content = dead_letter_file.read_text()
        dead_letter_event = json.loads(content.strip())
        assert "_error" in dead_letter_event
        assert dead_letter_event["_error"]
