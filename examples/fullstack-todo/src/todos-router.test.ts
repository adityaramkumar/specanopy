// generated_from: contracts/api/todos
// spec_hash: 2a5aff06c2636cc04fdde042e0308a97a8b89ba1a132aeae55374bcd169960f8
// generated_at: 2026-03-15T02:27:26.975193+00:00
// agent: implementation-agent
import { describe, it, expect, beforeEach } from 'vitest';
import request from 'supertest';
import express from 'express';
import { createTodosRouter } from './todos-router.js';

import type { TodosService } from './todos-service.js';
import type { Todo } from './todo.js';

const mockService: jest.Mocked<TodosService> = {
  getTodos: jest.fn(),
  createTodo: jest.fn(),
  updateTodo: jest.fn(),
  deleteTodo: jest.fn(),
};

const app = express();
app.use(express.json());
app.use('/api', createTodosRouter(mockService));

const requestApp = request(app);

describe('Todos Router', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /api/todos', () => {
    it('returns todos without filter', async () => {
      const mockTodos: Todo[] = [
        { id: '1', title: 'Test', completed: false, created_at: '2023-01-01T00:00:00Z', updated_at: '2023-01-01T00:00:00Z' }
      ];
      mockService.getTodos.mockResolvedValue({ todos: mockTodos, count: 1 });

      const res = await requestApp.get('/api/todos');
      expect(res.status).toBe(200);
      expect(res.body).toEqual({ todos: mockTodos, count: 1 });
      expect(mockService.getTodos).toHaveBeenCalledWith(undefined);
    });

    it('filters by completed=true', async () => {
      mockService.getTodos.mockResolvedValue({ todos: [], count: 0 });

      await requestApp.get('/api/todos?completed=true');
      expect(mockService.getTodos).toHaveBeenCalledWith({ completed: true });
    });

    it('filters by completed=false', async () => {
      mockService.getTodos.mockResolvedValue({ todos: [], count: 0 });

      await requestApp.get('/api/todos?completed=false');
      expect(mockService.getTodos).toHaveBeenCalledWith({ completed: false });
    });
  });

  describe('POST /api/todos', () => {
    it('creates todo successfully', async () => {
      const mockTodo: Todo = {
        id: '1',
        title: 'New Todo',
        completed: false,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
      };
      mockService.createTodo.mockResolvedValue(mockTodo);

      const res = await requestApp.post('/api/todos').send({ title: 'New Todo' });
      expect(res.status).toBe(201);
      expect(res.body).toEqual(mockTodo);
    });

    it('returns 422 title_required', async () => {
      const res = await requestApp.post('/api/todos').send({ title: '' });
      expect(res.status).toBe(422);
      expect(res.body).toEqual({ error: 'title_required' });
    });

    it('returns 422 title_too_long', async () => {
      const longTitle = 'a'.repeat(201);
      const res = await requestApp.post('/api/todos').send({ title: longTitle });
      expect(res.status).toBe(422);
      expect(res.body).toEqual({ error: 'title_too_long' });
    });
  });

  describe('PUT /api/todos/:id', () => {
    it('updates todo successfully', async () => {
      const mockTodo: Todo = {
        id: '1',
        title: 'Updated',
        completed: true,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-02T00:00:00Z',
      };
      mockService.updateTodo.mockResolvedValue(mockTodo);

      const res = await requestApp.put('/api/todos/1').send({ title: 'Updated', completed: true });
      expect(res.status).toBe(200);
      expect(res.body).toEqual(mockTodo);
    });

    it('returns 404 todo_not_found', async () => {
      mockService.updateTodo.mockResolvedValue(null);

      const res = await requestApp.put('/api/todos/1').send({ title: 'Updated' });
      expect(res.status).toBe(404);
      expect(res.body).toEqual({ error: 'todo_not_found' });
    });

    it('returns 422 title_too_long', async () => {
      const longTitle = 'a'.repeat(201);
      const res = await requestApp.put('/api/todos/1').send({ title: longTitle });
      expect(res.status).toBe(422);
      expect(res.body).toEqual({ error: 'title_too_long' });
    });
  });

  describe('DELETE /api/todos/:id', () => {
    it('deletes successfully', async () => {
      mockService.deleteTodo.mockResolvedValue(true);

      const res = await requestApp.delete('/api/todos/1');
      expect(res.status).toBe(204);
      expect(res.body).toBeDefined();
    });

    it('returns 404 todo_not_found', async () => {
      mockService.deleteTodo.mockResolvedValue(false);

      const res = await requestApp.delete('/api/todos/1');
      expect(res.status).toBe(404);
      expect(res.body).toEqual({ error: 'todo_not_found' });
    });
  });
});
