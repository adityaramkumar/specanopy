---
id: contracts/formats/csv
version: "1.0.0"
status: approved
---

## CSV Format Contract

### Structure
- First row is always the header row containing column names
- Delimiter: comma (`,`)
- Quoting: fields containing commas, newlines, or double quotes must be enclosed in double quotes
- Escape: double quotes within quoted fields are escaped by doubling (`""`)
- Encoding: UTF-8
- Line endings: `\n` (Unix-style)

### Constraints
- Maximum file size: 100 MB
- Maximum columns: 1000
- Maximum row length: 1 MB
- Column names must be unique (case-insensitive comparison)
- Empty files (0 bytes) are invalid
- Files with only a header row and no data rows are valid
