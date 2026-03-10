---
id: contracts/schemas/processed
version: "1.0.0"
status: approved
---

## Processed Events Schema

### Processed Event Object
```json
{
  "event_id": "string (UUID, from raw event)",
  "event_type": "string (from raw event)",
  "timestamp_utc": "string (ISO 8601, always UTC, no timezone offset)",
  "date": "string (YYYY-MM-DD, derived from timestamp_utc)",
  "hour": "integer (0-23, derived from timestamp_utc)",
  "user_id": "string (UUID or 'anonymous')",
  "is_anonymous": "boolean",
  "source": "string (from raw event)",
  "properties": "object (from raw event)",
  "enrichments": {
    "session_id": "string (UUID, assigned during transform)",
    "event_sequence": "integer (position within session)"
  }
}
```

### Output format
- Partitioned by date: `output/{date}/events.ndjson`
- Each partition file contains events sorted by `timestamp_utc` ascending
- Maximum partition file size: 256 MB (split into numbered files if exceeded)

### Session assignment rules
- Events from the same `user_id` within 30 minutes of each other belong to the same session
- Anonymous events (`user_id` is null) each get their own unique session
- Session IDs are deterministic UUIDs derived from `user_id + session_start_timestamp`
