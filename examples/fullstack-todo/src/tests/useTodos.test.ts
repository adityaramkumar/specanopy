// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.731380+00:00
// agent: testing-agent
// useTodos.test.ts
import { renderHook, act } from '@testing-library/react';
import { useTodos, UseTodosReturn, Todo, Filter, TodosState } from '../useTodos';
import { fetchTodos, createTodo, updateTodo, deleteTodo } from '../api-client';
import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('../api-client');

const mockTodo1: Todo = {
  id: '1',
  title: 'Test Todo 1',
  completed: false,
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z'
};

const mockTodo2: Todo = {
  id: '2',
  title: 'Test Todo 2',
  completed: true,
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z'
};

const mockTodosResponse = {
  todos: [mockTodo1, mockTodo2],
  count: 2
};

describe('useTodos', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('initializes with loading state and fetches todos on mount', async () => {
    (fetchTodos as any).mockResolvedValue(mockTodosResponse);

    const { result } = renderHook(() => useTodos());

    expect(result.current.state).toBe('loading');
    expect(result.current.todos).toEqual([]);
    expect(result.current.filteredTodos).toEqual([]);
    expect(result.current.filter).toBe('all');

    await act(async () => {
      // Wait for initial fetch
    });

    expect(fetchTodos).toHaveBeenCalledTimes(1);
    expect(result.current.state).toBe('success');
    expect(result.current.todos).toEqual(mockTodosResponse.todos);
    expect(result.current.filteredTodos).toEqual(mockTodosResponse.todos);
  });

  it('handles initial fetch error and sets error state', async () => {
    const mockError = new Error('Network error');
    (fetchTodos as any).mockRejectedValue(mockError);

    const { result } = renderHook(() => useTodos());

    await act(async () => {
      // Wait for initial fetch
    });

    expect(result.current.state).toBe('error');
    expect(result.current.error).toBeTruthy();
    expect(result.current.todos).toEqual([]);
  });

  it('refresh triggers fetchTodos and updates state', async () => {
    (fetchTodos as any).mockResolvedValue(mockTodosResponse);

    const { result } = renderHook(() => useTodos());
    await act(async () => {});

    const newTodosResponse = {
      todos: [{ ...mockTodo1, title: 'Updated' }],
      count: 1
    };
    (fetchTodos as any).mockResolvedValueOnce(newTodosResponse);

    await act(async () => {
      await result.current.refresh();
    });

    expect(fetchTodos).toHaveBeenCalledTimes(2);
    expect(result.current.todos).toEqual(newTodosResponse.todos);
  });

  it('addTodo creates todo and prepends to local state on success', async () => {
    (fetchTodos as any).mockResolvedValue(mockTodosResponse);
    const newTodo: Todo = {
      id: '3',
      title: 'New Todo',
      completed: false,
      created_at: '2023-01-02T00:00:00Z',
      updated_at: '2023-01-02T00:00:00Z'
    };
    (createTodo as any).mockResolvedValue(newTodo);

    const { result } = renderHook(() => useTodos());
    await act(async () => {});

    await act(async () => {
      await result.current.addTodo('New Todo');
    });

    expect(createTodo).toHaveBeenCalledWith('New Todo');
    expect(result.current.todos[0]).toEqual(newTodo);
    expect(result.current.todos.length).toBe(3);
    expect(result.current.addError).toBeNull();
  });

  it('addTodo handles creation error without crashing', async () => {
    (fetchTodos as any).mockResolvedValue(mockTodosResponse);
    (createTodo as any).mockRejectedValue(new Error('Validation error'));

    const { result } = renderHook(() => useTodos());
    await act(async () => {});

    await act(async () => {
      await result.current.addTodo('Invalid Todo');
    });

    expect(result.current.todos).toEqual(mockTodosResponse.todos);
    expect(result.current.addError).toBeNull();
  });

  it('toggleTodo performs optimistic update and reverts on error', async () => {
    (fetchTodos as any).mockResolvedValue({ todos: [mockTodo1], count: 1 });
    (updateTodo as any).mockRejectedValue(new Error('Update failed'));

    const { result } = renderHook(() => useTodos());
    await act(async () => {});

    // Optimistic update
    act(() => {
      result.current.toggleTodo('1');
    });

    expect(result.current.todos[0].completed).toBe(true);

    await act(async () => {
      // Wait for failed API call
    });

    expect(result.current.todos[0].completed).toBe(false);
  });

  it('deleteTodo performs optimistic delete and re-inserts on error', async () => {
    (fetchTodos as any).mockResolvedValue({ todos: [mockTodo1, mockTodo2], count: 2 });
    (deleteTodo as any).mockRejectedValue(new Error('Delete failed'));

    const { result } = renderHook(() => useTodos());
    await act(async () => {});

    const initialTodos = result.current.todos;

    // Optimistic delete
    act(() => {
      result.current.deleteTodo('1');
    });

    expect(result.current.todos.length).toBe(1);
    expect(result.current.todos[0]).toEqual(mockTodo2);

    await act(async () => {
      // Wait for failed API call
    });

    expect(result.current.todos).toEqual(initialTodos);
  });

  it('setFilter updates filter state and filteredTodos immediately', async () => {
    (fetchTodos as any).mockResolvedValue(mockTodosResponse);

    const { result } = renderHook(() => useTodos());
    await act(async () => {});

    act(() => {
      result.current.setFilter('active');
    });

    expect(result.current.filter).toBe('active');
    expect(result.current.filteredTodos).toEqual([mockTodo1]);

    act(() => {
      result.current.setFilter('completed');
    });

    expect(result.current.filter).toBe('completed');
    expect(result.current.filteredTodos).toEqual([mockTodo2]);
  });

  it('filtering shows correct todos for each filter type', async () => {
    (fetchTodos as any).mockResolvedValue(mockTodosResponse);

    const { result } = renderHook(() => useTodos());
    await act(async () => {});

    act(() => result.current.setFilter('all'));
    expect(result.current.filteredTodos.length).toBe(2);

    act(() => result.current.setFilter('active'));
    expect(result.current.filteredTodos.length).toBe(1);
    expect(result.current.filteredTodos[0].id).toBe('1');

    act(() => result.current.setFilter('completed'));
    expect(result.current.filteredTodos.length).toBe(1);
    expect(result.current.filteredTodos[0].id).toBe('2');
  });

  it('blocks concurrent actions on same todo during pending operations', async () => {
    (fetchTodos as any).mockResolvedValue({ todos: [mockTodo1], count: 1 });
    const pendingPromise = new Promise(() => {}); // Never resolves
    (updateToggle as any).mockReturnValue(pendingPromise);

    const { result } = renderHook(() => useTodos());
    await act(async () => {});

    // First toggle starts pending
    act(() => {
      result.current.toggleTodo('1');
    });

    // Second toggle on same todo should be blocked/queued
    act(() => {
      result.current.toggleTodo('1');
    });

    expect(updateTodo).toHaveBeenCalledTimes(1);
  });
});