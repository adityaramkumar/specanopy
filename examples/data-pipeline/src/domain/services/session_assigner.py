# generated_from: contracts/schemas/processed
# spec_hash: 363cd030c1920e3fa5120a35d07ebe130a62a4e292bbc5d4b4f784afb869fbf9
# generated_at: 2026-03-10T09:07:01.356779+00:00
# agent: implementation-agent

import uuid
from datetime import datetime

class SessionAssigner:
    def get_session_id(self, user_id: str, session_start: str) -> str:
        # deterministic UUID v5 style approach using namespace
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{user_id}_{session_start}"))

    def assign_session(self, user_id: str, timestamp_utc: str, last_event_time: str = None) -> str:
        if user_id == 'anonymous':
            return str(uuid.uuid4())
        
        # logic for 30-minute window check
        if last_event_time:
            curr = datetime.fromisoformat(timestamp_utc.replace('Z', '+00:00'))
            prev = datetime.fromisoformat(last_event_time.replace('Z', '+00:00'))
            if (curr - prev).total_seconds() <= 1800:
                return self.get_session_id(user_id, last_event_time)
        
        return self.get_session_id(user_id, timestamp_utc)