---
depends_on:
- contracts/api/todos
- contracts/ui/components
id: behaviors/frontend/todo-list
status: approved
version: 1.0.0
---

## Todo List Page Behavior

### Data Structures
- Todo Item: { id: string, title: string, completed: boolean }
- API GET /api/todos: Returns { data: TodoItem[] }
- API POST /api/todos: Accepts { title: string }, returns { data: TodoItem }
- API PUT /api/todos/:id: Accepts { completed: boolean }, returns { data: TodoItem }
- API DELETE /api/todos/:id: Returns 204 No Content

### Initial Load
- On mount, perform GET /api/todos.
- State 'Loading': Render a <div> with text 'Loading...'.
- State 'Error': Render a <div> with text 'Failed to load todos. Try again.' containing a <button> labeled 'Retry'. Clicking 'Retry' must trigger a fetch of /api/todos in-place without reloading the browser window.
- State 'Success': Render a <ul> of TodoItems.

### Adding a Todo
- Submit AddTodoForm: POST /api/todos with payload { title: string }.
- On Success (2xx): Prepend the new todo returned by the API to the local state. Clear the form input.
- On Error (non-2xx): Render a <span> with text 'Failed to add todo' immediately following the form. This message must be removed upon the next form submission attempt.

### Toggling Completion
- User clicks checkbox: Toggle local state immediately (optimistic).
- Perform PUT /api/todos/:id with { completed: !current }.
- On Error: Revert local state to previous value and call window.alert('Failed to update todo').

### Deleting a Todo
- User clicks delete: Remove item from local state immediately (optimistic).
- Perform DELETE /api/todos/:id.
- On Error: Re-insert item at its original index and call window.alert('Failed to delete todo').

### Filtering
- Filter options: 'All' (default), 'Active' (completed: false), 'Completed' (completed: true).
- Selection must update state and re-render the list immediately based on current local todos.
- Filtering logic is strictly client-side.

### Concurrency
- If an action (toggle/delete) is pending, subsequent actions on the same item must be blocked or queued by the UI until the pending request resolves.