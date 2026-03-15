# generated_from: behaviors/ingest
# spec_hash: a46bf4c24197a3b855328de74eab6c7676c144c326dc88fd066bc5484a1f8221
# generated_at: 2026-03-15T02:32:11.597613+00:00
# agent: implementation-agent
import pytest
import tempfile
import json
from pathlib import Path
from event_processor import process_ndjson_file, write_event_valid, write_event_dead_letter
from schemas.raw_events import RawEvent

@pytest.fixture
def valid_event():
    from schemas.raw_events import RawEvent
import uuid
    return RawEvent(
        event_id=str(uuid.uuid4()),
        event_type="page_view",
        timestamp="2023-01-01T12:00:00Z",
        user_id=None,
        properties={"test": True},
        source="web"
    )

@pytest.fixture
def invalid_event():
    return {"event_id": "invalid", "event_type": "invalid"}

class TestEventProcessor:
    def test_process_ndjson_file_mixed(self, tmp_path):
        input_file = tmp_path / "input.ndjson"
        input_file.write_text('{"event_id": "123e4567-e89b-12d3-a456-426614174000", "event_type": "page_view", "timestamp": "2023-01-01T12:00:00Z", "properties": {}, "source": "web"}\n{"invalid": true}\n')
        
        valid_output = tmp_path / "valid" / "events.ndjson"
        dead_letter_output = tmp_path / "dead-letter" / "events.ndjson"
        
        valid_dir = tmp_path / "valid"
        dead_letter_dir = tmp_path / "dead-letter"
        valid_dir.mkdir()
        dead_letter_dir.mkdir()
        
        result = process_ndjson_file(input_file, valid_output, dead_letter_output)
        
        assert result == (1, 1)
        assert valid_output.read_text().strip().endswith('}')  # has content
        assert dead_letter_output.read_text().strip().endswith('_error')  # has error

    def test_write_event_valid(self, tmp_path, valid_event):
        output_path = tmp_path / "valid" / "events.ndjson"
        output_path.parent.mkdir()
        
        write_event_valid(valid_event, output_path)
        
        content = output_path.read_text()
        assert json.loads(content.strip()) == valid_event.dict()

    def test_write_event_dead_letter(self, tmp_path):
        event_json = {"invalid": "event"}
        error = "validation error"
        output_path = tmp_path / "dead-letter" / "events.ndjson"
        output_path.parent.mkdir()
        
        write_event_dead_letter(event_json, error, output_path)
        
        content = output_path.read_text()
        dead_letter_event = json.loads(content.strip())
        assert dead_letter_event["invalid"] == "event"
        assert dead_letter_event["_error"] == error
