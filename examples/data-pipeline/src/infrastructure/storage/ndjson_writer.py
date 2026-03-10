# generated_from: contracts/schemas/processed
# spec_hash: 363cd030c1920e3fa5120a35d07ebe130a62a4e292bbc5d4b4f784afb869fbf9
# generated_at: 2026-03-10T09:07:01.356779+00:00
# agent: implementation-agent

import json
from dataclasses import asdict
from domain.models.processed_event import ProcessedEvent

class NDJSONWriter:
    def write(self, file_path: str, event: ProcessedEvent):
        with open(file_path, 'a') as f:
            f.write(json.dumps(asdict(event)) + '\n')