// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.733552+00:00
// agent: testing-agent
// api-client.test.ts
import { fetchTodos, createTodo, updateTodo, deleteTodo } from '../api-client';
import { describe, it, expect, vi } from 'vitest';

describe('api-client', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('fetchTodos calls GET /api/todos and returns parsed response', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue({ todos: [], count: 0 })
    } as Response);
    global.fetch = mockFetch;

    const result = await fetchTodos();

    expect(mockFetch).toHaveBeenCalledWith('/api/todos', {
      method: 'GET'
    });
    expect(result).toEqual({ todos: [], count: 0 });
  });

  it('fetchTodos throws Error on non-2xx response', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Server Error'
    } as Response);
    global.fetch = mockFetch;

    await expect(fetchTodos()).rejects.toThrow(Error);
  });

  it('createTodo calls POST /api/todos with title payload', async () => {
    const mockTodo = { id: '1', title: 'Test', completed: false, created_at: '', updated_at: '' };
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: vi.fn().mockResolvedValue(mockTodo)
    } as Response);
    global.fetch = mockFetch;

    const result = await createTodo('Test');

    expect(mockFetch).toHaveBeenCalledWith('/api/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'Test' })
    });
    expect(result).toEqual(mockTodo);
  });

  it('updateTodo calls PUT /api/todos/:id with updates payload', async () => {
    const mockTodo = { id: '1', title: 'Test', completed: true, created_at: '', updated_at: '' };
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue(mockTodo)
    } as Response);
    global.fetch = mockFetch;

    const result = await updateTodo('1', { completed: true });

    expect(mockFetch).toHaveBeenCalledWith('/api/todos/1', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: true })
    });
    expect(result).toEqual(mockTodo);
  });

  it('deleteTodo calls DELETE /api/todos/:id', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 204
    } as Response);
    global.fetch = mockFetch;

    await deleteTodo('1');

    expect(mockFetch).toHaveBeenCalledWith('/api/todos/1', {
      method: 'DELETE'
    });
  });

  it('api functions throw Error on non-2xx responses', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
      statusText: 'Not Found'
    } as Response);
    global.fetch = mockFetch;

    await expect(createTodo('Test')).rejects.toThrow(Error);
    await expect(updateTodo('1', { completed: true })).rejects.toThrow(Error);
    await expect(deleteTodo('1')).rejects.toThrow(Error);
  });
});