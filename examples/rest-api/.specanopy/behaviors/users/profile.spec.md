---
id: behaviors/users/profile
version: "1.0.0"
status: approved
depends_on:
  - contracts/api/users
---

## User Profile Behavior

### GET /api/users/:id

**Happy Path:**
- Authenticated user requests their own profile
- Return HTTP 200 with user object: `{ "id": "uuid", "email": "string", "name": "string", "created_at": "ISO 8601" }`
- Password hash is never included in the response

**Error Handling:**
- Unauthenticated request (no valid JWT): return HTTP 401 with `{ "error": "unauthorized" }`
- User not found: return HTTP 404 with `{ "error": "user_not_found" }`
- Requesting another user's profile: return HTTP 403 with `{ "error": "forbidden" }`

### PUT /api/users/:id

**Happy Path:**
- Authenticated user updates their own name
- Request body: `{ "name": "string" }`
- Return HTTP 200 with updated user object
- Email cannot be changed via this endpoint

**Error Handling:**
- Empty name: return HTTP 422 with `{ "error": "name_required" }`
- Name longer than 100 characters: return HTTP 422 with `{ "error": "name_too_long" }`
- Updating another user's profile: return HTTP 403 with `{ "error": "forbidden" }`
