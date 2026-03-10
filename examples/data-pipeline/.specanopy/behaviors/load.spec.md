---
id: behaviors/load
version: "1.0.0"
status: approved
depends_on:
  - contracts/schemas/processed
---

## Load Behavior

### Command
```
pipeline load <transform_dir> --output <output_dir>
```

### Happy Path
- Read all events from `transform_dir/events.ndjson`
- Partition by `date` field: create `output_dir/{date}/events.ndjson`
- Within each partition: events sorted by `timestamp_utc` ascending
- If a partition exceeds 256 MB: split into `events_001.ndjson`, `events_002.ndjson`, etc.
- Print summary: `Loaded {count} events into {partition_count} partitions`
- Exit code: 0

### Error Handling
- Transform directory not found: print `Error: directory not found: {path}` to stderr, exit code 1
- No events file: print `Error: no events found in {path}` to stderr, exit code 1
- Output directory already has partitions for a date: overwrite the existing partition files

### Idempotency
- Running load twice with the same input produces identical output
- Partition files are written atomically: write to `.tmp` then rename
