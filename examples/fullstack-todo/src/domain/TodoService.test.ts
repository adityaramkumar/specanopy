// generated_from: behaviors/backend/crud
// spec_hash: 3bc5a2b2d95a1b99ae840d8085c5ad9eb0e9da675c885ce816b5d22fbee68c88
// generated_at: 2026-03-15T02:27:52.038178+00:00
// agent: testing-agent
// domain/TodoService.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { TodoService } from './TodoService.js';
import type { Todo, TodoListResponse, ApiError } from './Todo.js';
import type { UuidAdapter } from '../adapters/UuidAdapter.js';
import type { DateAdapter } from '../adapters/DateAdapter.js';
import type { TodoStore } from './TodoStore.js';

describe('TodoService', () => {
  let mockUuidAdapter: UuidAdapter;
  let mockDateAdapter: DateAdapter;
  let mockTodoStore: TodoStore;
  let todoService: TodoService;
  const mockUuid = 'test-uuid-123';
  const mockNowIso = '2023-01-01T00:00:00.000Z';

  beforeEach(() => {
    mockUuidAdapter = { generate: vi.fn().mockReturnValue(mockUuid) };
    mockDateAdapter = { nowIso: vi.fn().mockReturnValue(mockNowIso) };
    mockTodoStore = {
      create: vi.fn(),
      findById: vi.fn(),
      findAll: vi.fn(),
      update: vi.fn(),
      delete: vi.fn(),
    };
    todoService = new TodoService(mockUuidAdapter, mockDateAdapter, mockTodoStore);
  });

  describe('create', () => {
    it('accepts title from input and generates UUID', async () => {
      const input = { title: 'Buy groceries' };
      const result = await todoService.create(input);

      expect(mockUuidAdapter.generate).toHaveBeenCalled();
      expect(result).toEqual({
        id: mockUuid,
        title: 'Buy groceries',
        completed: false,
        created_at: mockNowIso,
        updated_at: mockNowIso,
      });
      expect(mockTodoStore.create).toHaveBeenCalledWith(result);
    });

    it('sets completed to false', async () => {
      const input = { title: 'Test todo' };
      const result = await todoService.create(input);
      expect(result.completed).toBe(false);
    });

    it('sets created_at and updated_at to current UTC timestamp', async () => {
      const input = { title: 'Test todo' };
      const result = await todoService.create(input);
      expect(result.created_at).toBe(mockNowIso);
      expect(result.updated_at).toBe(mockNowIso);
      expect(mockDateAdapter.nowIso).toHaveBeenCalledTimes(2);
    });

    it('throws title_required for whitespace only title', async () => {
      const input = { title: ' ' };
      await expect(todoService.create(input)).rejects.toEqual({
        error: 'title_required',
      } as ApiError);
    });

    it('throws title_too_long if title exceeds 200 characters', async () => {
      const longTitle = 'a'.repeat(201);
      const input = { title: longTitle };
      await expect(todoService.create(input)).rejects.toEqual({
        error: 'title_too_long',
      } as ApiError);
    });
  });

  describe('list', () => {
    it('returns all todos sorted by created_at descending', async () => {
      const mockTodos: Todo[] = [
        { id: '2', title: 'old', completed: false, created_at: '2023-01-01T10:00:00Z', updated_at: '2023-01-01T10:00:00Z' },
        { id: '1', title: 'new', completed: false, created_at: '2023-01-01T12:00:00Z', updated_at: '2023-01-01T12:00:00Z' },
      ];
      vi.spyOn(mockTodoStore, 'findAll').mockResolvedValue(mockTodos);

      const result = await todoService.list();

      expect(mockTodoStore.findAll).toHaveBeenCalledWith(undefined);
      expect(result).toEqual({
        todos: mockTodos.reverse(),
        count: 2,
      } as TodoListResponse);
    });

    it('filters completed=true to return only completed todos', async () => {
      const mockTodos: Todo[] = [
        { id: '1', title: 'completed', completed: true, created_at: '2023-01-01T12:00:00Z', updated_at: '2023-01-01T12:00:00Z' },
        { id: '2', title: 'active', completed: false, created_at: '2023-01-01T10:00:00Z', updated_at: '2023-01-01T10:00:00Z' },
      ];
      vi.spyOn(mockTodoStore, 'findAll').mockResolvedValue(mockTodos);

      const result = await todoService.list(true);

      expect(mockTodoStore.findAll).toHaveBeenCalledWith(true);
      expect(result.todos.length).toBe(1);
      expect(result.todos[0].completed).toBe(true);
      expect(result.count).toBe(1);
    });

    it('filters completed=false to return only active todos', async () => {
      const mockTodos: Todo[] = [
        { id: '1', title: 'completed', completed: true, created_at: '2023-01-01T12:00:00Z', updated_at: '2023-01-01T12:00:00Z' },
        { id: '2', title: 'active', completed: false, created_at: '2023-01-01T10:00:00Z', updated_at: '2023-01-01T10:00:00Z' },
      ];
      vi.spyOn(mockTodoStore, 'findAll').mockResolvedValue(mockTodos);

      const result = await todoService.list(false);

      expect(mockTodoStore.findAll).toHaveBeenCalledWith(false);
      expect(result.todos.length).toBe(1);
      expect(result.todos[0].completed).toBe(false);
      expect(result.count).toBe(1);
    });

    it('includes count field with number of returned todos', async () => {
      const mockTodos: Todo[] = [{ id: '1', title: 'test', completed: false, created_at: '2023-01-01T12:00:00Z', updated_at: '2023-01-01T12:00:00Z' }];
      vi.spyOn(mockTodoStore, 'findAll').mockResolvedValue(mockTodos);

      const result = await todoService.list();
      expect(result.count).toBe(1);
    });
  });

  describe('update', () => {
    it('accepts partial updates for title and/or completed', async () => {
      const mockTodo: Todo = {
        id: 'test-id',
        title: 'old title',
        completed: false,
        created_at: '2023-01-01T12:00:00Z',
        updated_at: '2023-01-01T12:00:00Z',
      };
      vi.spyOn(mockTodoStore, 'findById').mockResolvedValue(mockTodo);
      vi.spyOn(mockTodoStore, 'update').mockResolvedValue();

      const input = { title: 'new title', completed: true };
      const result = await todoService.update('test-id', input);

      expect(result).toEqual({
        ...mockTodo,
        title: 'new title',
        completed: true,
        updated_at: mockNowIso,
      });
      expect(mockTodoStore.update).toHaveBeenCalledWith(result);
      expect(mockDateAdapter.nowIso).toHaveBeenCalled();
    });

    it('updates updated_at to current UTC timestamp', async () => {
      const mockTodo: Todo = {
        id: 'test-id',
        title: 'old',
        completed: false,
        created_at: '2023-01-01T12:00:00Z',
        updated_at: '2023-01-01T10:00:00Z',
      };
      vi.spyOn(mockTodoStore, 'findById').mockResolvedValue(mockTodo);
      vi.spyOn(mockTodoStore, 'update').mockResolvedValue();

      await todoService.update('test-id', { completed: true });
      expect(mockDateAdapter.nowIso).toHaveBeenCalled();
    });

    it('throws todo_not_found if todo doesnt exist', async () => {
      vi.spyOn(mockTodoStore, 'findById').mockResolvedValue(null);

      await expect(todoService.update('nonexistent', {})).rejects.toEqual({
        error: 'todo_not_found',
      } as ApiError);
    });

    it('throws title_too_long if title exceeds 200 characters', async () => {
      const mockTodo: Todo = {
        id: 'test-id',
        title: 'old',
        completed: false,
        created_at: '2023-01-01T12:00:00Z',
        updated_at: '2023-01-01T12:00:00Z',
      };
      vi.spyOn(mockTodoStore, 'findById').mockResolvedValue(mockTodo);

      const longTitle = 'a'.repeat(201);
      await expect(todoService.update('test-id', { title: longTitle })).rejects.toEqual({
        error: 'title_too_long',
      } as ApiError);
    });
  });

  describe('delete', () => {
    it('removes todo from storage', async () => {
      vi.spyOn(mockTodoStore, 'delete').mockResolvedValue();

      await todoService.delete('test-id');

      expect(mockTodoStore.delete).toHaveBeenCalledWith('test-id');
    });

    it('throws todo_not_found if todo doesnt exist', async () => {
      vi.spyOn(mockTodoStore, 'delete').mockRejectedValue({
        error: 'todo_not_found',
      } as ApiError);

      await expect(todoService.delete('nonexistent')).rejects.toEqual({
        error: 'todo_not_found',
      } as ApiError);
    });
  });
});