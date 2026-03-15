// generated_from: behaviors/backend/crud
// spec_hash: 3bc5a2b2d95a1b99ae840d8085c5ad9eb0e9da675c885ce816b5d22fbee68c88
// generated_at: 2026-03-15T02:27:52.038640+00:00
// agent: testing-agent
// domain/TodoStore.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { TodoStore } from './TodoStore.js';
import type { Todo } from './Todo.js';

describe('TodoStore', () => {
  let todoStore: TodoStore;

  beforeEach(() => {
    todoStore = new TodoStore();
  });

  it('creates todo', async () => {
    const todo: Todo = {
      id: 'test-id',
      title: 'test',
      completed: false,
      created_at: '2023-01-01T12:00:00Z',
      updated_at: '2023-01-01T12:00:00Z',
    };

    await todoStore.create(todo);

    const found = await todoStore.findById('test-id');
    expect(found).toEqual(todo);
  });

  it('finds todo by id', async () => {
    const todo: Todo = {
      id: 'test-id',
      title: 'test',
      completed: false,
      created_at: '2023-01-01T12:00:00Z',
      updated_at: '2023-01-01T12:00:00Z',
    };
    await todoStore.create(todo);

    const found = await todoStore.findById('test-id');
    expect(found).toEqual(todo);
  });

  it('returns null for non-existent todo', async () => {
    const found = await todoStore.findById('nonexistent');
    expect(found).toBeNull();
  });

  it('finds all todos', async () => {
    const todos: Todo[] = [
      { id: '1', title: 'first', completed: false, created_at: '2023-01-01T12:00:00Z', updated_at: '2023-01-01T12:00:00Z' },
      { id: '2', title: 'second', completed: true, created_at: '2023-01-01T11:00:00Z', updated_at: '2023-01-01T11:00:00Z' },
    ];

    await todoStore.create(todos[0]);
    await todoStore.create(todos[1]);

    const all = await todoStore.findAll();
    expect(all).toHaveLength(2);
  });

  it('filters todos by completed status', async () => {
    const todos: Todo[] = [
      { id: '1', title: 'active', completed: false, created_at: '2023-01-01T12:00:00Z', updated_at: '2023-01-01T12:00:00Z' },
      { id: '2', title: 'completed', completed: true, created_at: '2023-01-01T11:00:00Z', updated_at: '2023-01-01T11:00:00Z' },
    ];

    await todoStore.create(todos[0]);
    await todoStore.create(todos[1]);

    const active = await todoStore.findAll(false);
    expect(active).toHaveLength(1);
    expect(active[0].completed).toBe(false);

    const completed = await todoStore.findAll(true);
    expect(completed).toHaveLength(1);
    expect(completed[0].completed).toBe(true);
  });

  it('updates todo', async () => {
    const original: Todo = {
      id: 'test-id',
      title: 'original',
      completed: false,
      created_at: '2023-01-01T12:00:00Z',
      updated_at: '2023-01-01T12:00:00Z',
    };
    const updated: Todo = {
      ...original,
      title: 'updated',
      completed: true,
      updated_at: '2023-01-01T13:00:00Z',
    };

    await todoStore.create(original);
    await todoStore.update(updated);

    const found = await todoStore.findById('test-id');
    expect(found).toEqual(updated);
  });

  it('deletes todo', async () => {
    const todo: Todo = {
      id: 'test-id',
      title: 'test',
      completed: false,
      created_at: '2023-01-01T12:00:00Z',
      updated_at: '2023-01-01T12:00:00Z',
    };
    await todoStore.create(todo);

    await todoStore.delete('test-id');

    const found = await todoStore.findById('test-id');
    expect(found).toBeNull();
  });
});