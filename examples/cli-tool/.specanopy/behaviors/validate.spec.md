---
id: behaviors/validate
version: "1.0.0"
status: approved
depends_on:
  - contracts/formats/csv
---

## Validate Behavior

### Command
```
csvjson validate <input.csv>
```

### Happy Path
- Read and parse the CSV file
- Check all constraints from the CSV format contract
- If valid: print `Valid: {N} rows, {M} columns` to stdout, exit code 0

### Validation checks (in order)
1. File exists and is readable
2. File is not empty (0 bytes)
3. File size does not exceed 100 MB
4. Header row is present and parseable
5. Column names are unique (case-insensitive)
6. Column count does not exceed 1000
7. Each data row has the same number of fields as the header
8. No row exceeds 1 MB in length
9. All quoting is properly closed

### Error reporting
- On first error found: print `Invalid: {description} at line {N}` to stderr, exit code 1
- Only report the first error (fail-fast)
