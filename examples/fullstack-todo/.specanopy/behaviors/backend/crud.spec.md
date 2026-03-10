---
id: behaviors/backend/crud
version: "1.0.0"
status: approved
depends_on:
  - contracts/api/todos
---

## Todo CRUD Behavior

### Create
- Accept title from request body
- Generate UUID for id
- Set `completed` to `false`
- Set `created_at` and `updated_at` to current UTC timestamp
- Store in memory (no database for this example)
- Return the created todo with HTTP 201

### Read (list)
- Return all todos sorted by `created_at` descending (newest first)
- If `?completed=true`: return only completed todos
- If `?completed=false`: return only active todos
- Include `count` field with the number of returned todos

### Update
- Accept partial updates: `title` and/or `completed`
- Update `updated_at` to current UTC timestamp on any change
- Return the full updated todo with HTTP 200
- Do not allow updating `id`, `created_at`

### Delete
- Remove todo from storage
- Return HTTP 204 with no body
- Deleting a non-existent todo returns 404

### Edge Cases
- Creating a todo with title " " (whitespace only) returns 422 with `{ "error": "title_required" }`
- Updating with an empty object (no fields) returns the todo unchanged with HTTP 200
