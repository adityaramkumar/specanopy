// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.730155+00:00
// agent: implementation-agent
import { renderHook, act } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { useTodos } from './useTodos.js';
import * as apiClient from './api-client.js';

const mockTodo = {
  id: '1',
  title: 'Test Todo',
  completed: false,
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z',
};

const mockTodosResponse = { todos: [mockTodo], count: 1 };

vi.mock('./api-client.js', () => ({
  fetchTodos: vi.fn(),
  createTodo: vi.fn(),
  updateTodo: vi.fn(),
  deleteTodo: vi.fn(),
}));

describe('useTodos', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(window, 'alert').mockImplementation(() => {});
  });

  it('initializes with loading state and fetches todos', async () => {
    (apiClient.fetchTodos as ReturnType<typeof vi.fn>).mockResolvedValue(mockTodosResponse);

    const { result } = renderHook(() => useTodos());

    expect(result.current.state).toBe('loading');

    await act(async () => {
      await new Promise(process.nextTick);
    });

    expect(apiClient.fetchTodos).toHaveBeenCalled();
    expect(result.current.state).toBe('success');
    expect(result.current.todos).toEqual([mockTodo]);
  });

  it('handles toggle optimistic update and revert on error', async () => {
    (apiClient.fetchTodos as ReturnType<typeof vi.fn>).mockResolvedValue(mockTodosResponse);
    (apiClient.updateTodo as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('Failed'));

    const { result } = renderHook(() => useTodos());

    await act(async () => {
      await new Promise(process.nextTick);
    });

    await act(async () => {
      await result.current.toggleTodo('1');
    });

    expect(result.current.todos[0].completed).toBe(true);

    await act(async () => {
      // Wait for error handling
      await new Promise(process.nextTick);
    });

    expect(result.current.todos[0].completed).toBe(false);
    expect(window.alert).toHaveBeenCalledWith('Failed to update todo');
  });

  it('blocks concurrent toggle operations', async () => {
    (apiClient.fetchTodos as ReturnType<typeof vi.fn>).mockResolvedValue(mockTodosResponse);
    (apiClient.updateTodo as ReturnType<typeof vi.fn>).mockResolvedValue(mockTodo);

    const { result } = renderHook(() => useTodos());

    await act(async () => {
      await new Promise(process.nextTick);
    });

    await act(async () => {
      const firstToggle = result.current.toggleTodo('1');
      const secondToggle = result.current.toggleTodo('1');
      await firstToggle;
    });

    expect(apiClient.updateTodo).toHaveBeenCalledTimes(1);
  });
});