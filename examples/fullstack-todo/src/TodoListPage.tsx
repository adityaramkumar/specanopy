// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.728788+00:00
// agent: implementation-agent
import { FC, useState } from 'react';
import { useTodos, type UseTodosReturn, type Filter } from './useTodos.js';
import { TodoList } from './ui/TodoList';
import { AddTodoForm } from './ui/AddTodoForm';
import { TodoFilter } from './ui/TodoFilter';

export const TodoListPage: FC = () => {
  const {
    todos,
    filteredTodos,
    filter,
    state,
    error,
    addError,
    refresh,
    addTodo,
    toggleTodo,
    deleteTodo,
    setFilter,
  } = useTodos();

  const [retryKey, setRetryKey] = useState(0);

  const handleRetry = async () => {
    setRetryKey(prev => prev + 1);
    await refresh();
  };

  if (state === 'loading') {
    return <div>Loading...</div>;
  }

  if (state === 'error') {
    return (
      <div>
        <div>Failed to load todos. Try again.</div>
        <button onClick={handleRetry}>Retry</button>
      </div>
    );
  }

  return (
    <div>
      <TodoFilter filter={filter} onChange={setFilter} />
      <AddTodoForm onAdd={addTodo} error={addError} />
      <TodoList todos={filteredTodos} onToggle={toggleTodo} onDelete={deleteTodo} />
    </div>
  );
};