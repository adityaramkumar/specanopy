---
id: behaviors/ingest
version: "1.0.0"
status: approved
depends_on:
  - contracts/schemas/raw-events
---

## Ingest Behavior

### Command
```
pipeline ingest <input_dir> --output <staging_dir>
```

### Happy Path
- Scan `input_dir` for all `*.ndjson` files
- For each file: read line by line, validate each event against the raw events schema
- Valid events: write to `staging_dir/valid/events.ndjson`
- Invalid events: write to `staging_dir/dead-letter/events.ndjson` with an additional `_error` field describing the validation failure
- Print summary to stdout: `Ingested {valid_count} events, {invalid_count} rejected, from {file_count} files`
- Exit code: 0

### Error Handling
- Input directory not found: print `Error: directory not found: {path}` to stderr, exit code 1
- No NDJSON files found: print `Error: no .ndjson files in {path}` to stderr, exit code 1
- Malformed JSON line (not parseable): write to dead-letter with `_error: "malformed JSON at line {N}"`
- Event exceeding 64 KB: write to dead-letter with `_error: "event too large: {size} bytes"`

### Edge Cases
- Empty files (0 bytes) are skipped silently
- Files with only invalid events produce an empty valid output and a populated dead-letter output
