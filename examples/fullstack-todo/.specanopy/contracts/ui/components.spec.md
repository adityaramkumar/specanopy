---
id: contracts/ui/components
version: "1.0.0"
status: approved
depends_on:
  - contracts/api/todos
---

## UI Component Contract

### TodoItem Component
- Props: `{ todo: Todo, onToggle: (id: string) => void, onDelete: (id: string) => void }`
- Renders: checkbox (checked = todo.completed), title text, delete button
- Checkbox toggle calls `onToggle(todo.id)`
- Delete button calls `onDelete(todo.id)`
- Completed todos render title with strikethrough style

### TodoList Component
- Props: `{ todos: Todo[], onToggle, onDelete }`
- Renders a list of `TodoItem` components
- Empty state: renders "No todos yet" text when list is empty

### AddTodoForm Component
- State: input text field
- On submit: calls `onAdd(title)` prop with trimmed input, clears input
- Disabled submit button when input is empty or whitespace-only
- Max length 200 enforced on input field

### TodoFilter Component
- Props: `{ filter: "all" | "active" | "completed", onChange: (filter) => void }`
- Renders three buttons: All, Active, Completed
- Active filter button has distinct visual style
