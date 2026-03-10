# generated_from: contracts/schemas/processed
# spec_hash: 363cd030c1920e3fa5120a35d07ebe130a62a4e292bbc5d4b4f784afb869fbf9
# generated_at: 2026-03-10T09:07:01.356779+00:00
# agent: implementation-agent

from domain.services.event_transformer import EventTransformer
from domain.services.session_assigner import SessionAssigner
from infrastructure.storage.file_partitioner import FilePartitioner
from infrastructure.storage.ndjson_writer import NDJSONWriter

class EventProcessor:
    def __init__(self):
        self.transformer = EventTransformer()
        self.assigner = SessionAssigner()
        self.partitioner = FilePartitioner()
        self.writer = NDJSONWriter()

    def process_events(self, raw_events: list):
        sorted_events = sorted(raw_events, key=lambda x: x['timestamp_utc'])
        session_map = {}
        
        for raw in sorted_events:
            user_id = raw.get('user_id') or 'anonymous'
            sid = self.assigner.assign_session(user_id, raw['timestamp_utc'], session_map.get(user_id))
            session_map[user_id] = raw['timestamp_utc']
            
            processed = self.transformer.transform(raw, sid, 1)
            path = self.partitioner.get_path(processed.date)
            self.writer.write(path, processed)