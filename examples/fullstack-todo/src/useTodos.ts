// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.727806+00:00
// agent: implementation-agent
import { useCallback, useState, useEffect, useRef } from 'react';
import type { Todo, TodosResponse, Filter, TodosState, TodoActionLock } from './types.js';
import { fetchTodos, createTodo, updateTodo, deleteTodo } from './api-client.js';

export interface UseTodosReturn {
  todos: Todo[];
  filteredTodos: Todo[];
  filter: Filter;
  state: TodosState;
  error: string | null;
  addError: string | null;
  refresh: () => Promise<void>;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
  setFilter: (filter: Filter) => void;
}

export function useTodos(): UseTodosReturn {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<Filter>('all');
  const [state, setState] = useState<TodosState>('loading');
  const [error, setError] = useState<string | null>(null);
  const [addError, setAddError] = useState<string | null>(null);
  const locksRef = useRef<Map<string, TodoActionLock>>(new Map());

  const getFilteredTodos = useCallback(() => {
    if (filter === 'active') return todos.filter(todo => !todo.completed);
    if (filter === 'completed') return todos.filter(todo => todo.completed);
    return todos;
  }, [todos, filter]);

  const isLocked = useCallback((id: string) => {
    return locksRef.current.has(id);
  }, []);

  const setLock = useCallback((id: string, type: 'toggle' | 'delete') => {
    locksRef.current.set(id, { id, type, pending: true });
  }, []);

  const clearLock = useCallback((id: string) => {
    locksRef.current.delete(id);
  }, []);

  const refresh = useCallback(async () => {
    setState('loading');
    setError(null);
    try {
      const response = await fetchTodos();
      setTodos(response.todos);
      setState('success');
    } catch (err) {
      setError('Failed to load todos');
      setState('error');
    }
  }, []);

  const addTodo = useCallback(async (title: string) => {
    setAddError(null);
    try {
      const newTodo = await createTodo(title);
      setTodos(prev => [newTodo, ...prev]);
    } catch (err) {
      setAddError('Failed to add todo');
      throw err;
    }
  }, []);

  const toggleTodo = useCallback(async (id: string) => {
    if (isLocked(id)) return;

    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    const prevCompleted = todo.completed;
    const newCompleted = !prevCompleted;

    setTodos(prev => prev.map(t => 
      t.id === id ? { ...t, completed: newCompleted } : t
    ));

    setLock(id, 'toggle');

    try {
      await updateTodo(id, { completed: newCompleted });
    } catch (err) {
      setTodos(prev => prev.map(t => 
        t.id === id ? { ...t, completed: prevCompleted } : t
      ));
      window.alert('Failed to update todo');
      throw err;
    } finally {
      clearLock(id);
    }
  }, [todos, isLocked, setLock, clearLock]);

  const deleteTodoFn = useCallback(async (id: string) => {
    if (isLocked(id)) return;

    const todoIndex = todos.findIndex(t => t.id === id);
    if (todoIndex === -1) return;

    const deletedTodo = todos[todoIndex];
    setTodos(prev => prev.filter(t => t.id !== id));

    setLock(id, 'delete');

    try {
      await deleteTodo(id);
    } catch (err) {
      setTodos(prev => [
        ...prev.slice(0, todoIndex),
        deletedTodo,
        ...prev.slice(todoIndex)
      ]);
      window.alert('Failed to delete todo');
      throw err;
    } finally {
      clearLock(id);
    }
  }, [todos, isLocked, setLock, clearLock]);

  useEffect(() => {
    refresh();
  }, []);

  return {
    todos,
    filteredTodos: getFilteredTodos(),
    filter,
    state,
    error,
    addError,
    refresh,
    addTodo,
    toggleTodo,
    deleteTodo: deleteTodoFn,
    setFilter,
  };
}