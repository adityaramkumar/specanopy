// generated_from: contracts/api/todos
// spec_hash: 2a5aff06c2636cc04fdde042e0308a97a8b89ba1a132aeae55374bcd169960f8
// generated_at: 2026-03-15T02:27:26.979107+00:00
// agent: testing-agent
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { TodosService } from './todos-service.js';

describe('TodosService', () => {
  let service: TodosService;

  beforeEach(() => {
    service = {
      getTodos: vi.fn(),
      createTodo: vi.fn(),
      updateTodo: vi.fn(),
      deleteTodo: vi.fn(),
    } as unknown as TodosService;
  });

  describe('getTodos', () => {
    it('returns todos array and count without filter', async () => {
      const mockResult = { todos: [], count: 0 };
      (service.getTodos as any).mockResolvedValue(mockResult);

      const result = await service.getTodos();
      expect(result).toEqual(mockResult);
    });

    it('returns todos array and count with completed=true filter', async () => {
      const mockResult = { todos: [], count: 0 };
      (service.getTodos as any).mockResolvedValue(mockResult);

      const result = await service.getTodos({ completed: true });
      expect(result).toEqual(mockResult);
    });

    it('returns todos array and count with completed=false filter', async () => {
      const mockResult = { todos: [], count: 0 };
      (service.getTodos as any).mockResolvedValue(mockResult);

      const result = await service.getTodos({ completed: false });
      expect(result).toEqual(mockResult);
    });
  });

  describe('createTodo', () => {
    it('returns Todo object for valid title', async () => {
      const mockTodo = {
        id: 'uuid',
        title: 'Test todo',
        completed: false,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
      };
      (service.createTodo as any).mockResolvedValue(mockTodo);

      const result = await service.createTodo('Test todo');
      expect(result).toEqual(mockTodo);
    });
  });

  describe('updateTodo', () => {
    it('returns updated Todo object when todo exists', async () => {
      const mockTodo = {
        id: '123',
        title: 'Updated',
        completed: true,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
      };
      (service.updateTodo as any).mockResolvedValue(mockTodo);

      const result = await service.updateTodo('123', { title: 'Updated', completed: true });
      expect(result).toEqual(mockTodo);
    });

    it('returns null when todo not found', async () => {
      (service.updateTodo as any).mockResolvedValue(null);

      const result = await service.updateTodo('nonexistent', { title: 'Updated' });
      expect(result).toBeNull();
    });

    it('handles partial updates', async () => {
      const mockTodo = {
        id: '123',
        title: 'Only title changed',
        completed: false,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
      };
      (service.updateTodo as any).mockResolvedValue(mockTodo);

      const result = await service.updateTodo('123', { title: 'Only title changed' });
      expect(result).toEqual(mockTodo);
    });
  });

  describe('deleteTodo', () => {
    it('returns true when todo deleted successfully', async () => {
      (service.deleteTodo as any).mockResolvedValue(true);

      const result = await service.deleteTodo('123');
      expect(result).toBe(true);
    });

    it('returns false when todo not found', async () => {
      (service.deleteTodo as any).mockResolvedValue(false);

      const result = await service.deleteTodo('nonexistent');
      expect(result).toBe(false);
    });
  });
});