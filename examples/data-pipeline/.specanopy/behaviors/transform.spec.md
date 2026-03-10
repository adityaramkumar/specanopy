---
id: behaviors/transform
version: "1.0.0"
status: approved
depends_on:
  - contracts/schemas/raw-events
  - contracts/schemas/processed
---

## Transform Behavior

### Command
```
pipeline transform <staging_dir> --output <transform_dir>
```

### Happy Path
- Read all events from `staging_dir/valid/events.ndjson`
- For each event:
  1. Normalize timestamp to UTC (strip timezone offset)
  2. Derive `date` (YYYY-MM-DD) and `hour` (0-23) from UTC timestamp
  3. Set `user_id` to `"anonymous"` if null; set `is_anonymous` to `true`/`false`
  4. Assign `session_id` and `event_sequence` per session assignment rules
- Sort all events by `timestamp_utc` ascending
- Write to `transform_dir/events.ndjson`
- Print summary: `Transformed {count} events, {session_count} sessions identified`
- Exit code: 0

### Session Assignment
- Group events by `user_id`
- Within each user's events (sorted by timestamp), start a new session when the gap between consecutive events exceeds 30 minutes
- Session ID: deterministic UUID v5 from namespace `6ba7b810-9dad-11d1-80b4-00c04fd430c8` with name `{user_id}:{session_start_timestamp}`
- `event_sequence`: 1-indexed position within the session

### Error Handling
- Staging directory not found: print `Error: directory not found: {path}` to stderr, exit code 1
- No valid events file: print `Error: no valid events found in {path}` to stderr, exit code 1
