---
id: behaviors/frontend/todo-list
version: "1.0.0"
status: approved
depends_on:
  - contracts/api/todos
  - contracts/ui/components
---

## Todo List Page Behavior

### Initial Load
- On mount, fetch all todos from GET /api/todos
- Display loading spinner while fetching
- On success, render TodoList with the returned todos
- On error, display "Failed to load todos. Try again." with a retry button

### Adding a Todo
- User types in AddTodoForm and submits
- POST /api/todos with the title
- On success: prepend new todo to the list (no full refetch)
- On error: display inline error "Failed to add todo" below the form

### Toggling Completion
- User clicks checkbox on a TodoItem
- PUT /api/todos/:id with `{ "completed": !current }` (optimistic update)
- On success: keep the toggled state
- On error: revert the toggle, display brief error toast

### Deleting a Todo
- User clicks delete button on a TodoItem
- Show confirmation: "Delete this todo?" with Cancel / Delete buttons
- On confirm: DELETE /api/todos/:id
- On success: remove from list
- On error: display brief error toast, keep todo in list

### Filtering
- TodoFilter at the top of the page
- "All" shows everything, "Active" shows `completed === false`, "Completed" shows `completed === true`
- Filter is client-side (no API call), applied to the already-fetched list
- Default filter on page load: "All"
