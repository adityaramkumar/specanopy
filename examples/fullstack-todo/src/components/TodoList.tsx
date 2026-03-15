// generated_from: contracts/ui/components
// spec_hash: bc79e30afe2aa54205d718240aef2c47fd0990937de675688ac674d7bdae57c0
// generated_at: 2026-03-15T02:28:11.276233+00:00
// agent: implementation-agent
import { Todo } from '../types/Todo';

export interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export function TodoList({ todos, onToggle, onDelete }: TodoListProps): JSX.Element {
  if (todos.length === 0) {
    return <div>No todos yet</div>;
  }

  return (
    <div>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}