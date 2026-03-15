// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.730714+00:00
// agent: implementation-agent
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { fetchTodos, createTodo, updateTodo, deleteTodo } from './api-client.js';

const mockFetch = vi.fn();
global.fetch = mockFetch as any;

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('fetchTodos handles success', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ todos: [], count: 0 }),
    } as Response);

    await expect(fetchTodos()).resolves.toEqual({ todos: [], count: 0 });
    expect(mockFetch).toHaveBeenCalledWith('/api/todos');
  });

  it('fetchTodos throws on error', async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 500,
      text: () => Promise.resolve('Server error'),
    } as Response);

    await expect(fetchTodos()).rejects.toThrow('HTTP 500: Server error');
  });

  it('createTodo sends POST and returns todo', async () => {
    const mockTodo = { id: '1', title: 'Test', completed: false, created_at: '', updated_at: '' };
    mockFetch.mockResolvedValue({
      ok: true,
      status: 201,
      json: () => Promise.resolve(mockTodo),
    } as Response);

    await expect(createTodo('Test')).resolves.toEqual(mockTodo);
    expect(mockFetch).toHaveBeenCalledWith('/api/todos', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ title: 'Test' }),
    }));
  });

  it('deleteTodo handles 204 success', async () => {
    mockFetch.mockResolvedValue({ ok: true, status: 204 } as Response);

    await expect(deleteTodo('1')).resolves.toBeUndefined();
    expect(mockFetch).toHaveBeenCalledWith('/api/todos/1', expect.objectContaining({
      method: 'DELETE',
    }));
  });
});