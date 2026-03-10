---
id: behaviors/convert
version: "1.0.0"
status: approved
depends_on:
  - contracts/formats/csv
  - contracts/formats/json
---

## Convert Behavior

### Command
```
csvjson <input.csv> [output.json]
```

### Happy Path
- Read CSV from `input.csv`
- Parse according to the CSV format contract
- Convert each row to a JSON object using column headers as keys
- Write JSON array to `output.json` (or stdout if no output file given)
- Print to stderr: `Converted {N} rows from {input} to {output}`
- Exit code: 0

### Error Handling
- Input file not found: print `Error: file not found: {path}` to stderr, exit code 1
- Input file is empty (0 bytes): print `Error: empty file: {path}` to stderr, exit code 1
- Malformed CSV (unclosed quote): print `Error: malformed CSV at line {N}: unclosed quote` to stderr, exit code 1
- Duplicate column names: print `Error: duplicate column name: {name}` to stderr, exit code 1
- File exceeds 100 MB: print `Error: file too large: {size} bytes (max 100 MB)` to stderr, exit code 1

### Flags
- `--detect-types`: enable type detection per the JSON format contract
- `--compact`: output compact JSON (no indentation)
