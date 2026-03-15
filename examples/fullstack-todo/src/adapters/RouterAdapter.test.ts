// generated_from: behaviors/backend/crud
// spec_hash: 3bc5a2b2d95a1b99ae840d8085c5ad9eb0e9da675c885ce816b5d22fbee68c88
// generated_at: 2026-03-15T02:27:52.037574+00:00
// agent: implementation-agent
import { describe, it, expect, beforeEach, vi } from 'vitest';
import request from 'supertest';
import express from 'express';
import { createTodoRouter } from './RouterAdapter.js';
import { TodoService } from '../domain/TodoService.js';

describe('RouterAdapter', () => {
  let app: express.Express;
  let todoService: TodoService;

  beforeEach(() => {
    todoService = {
      create: vi.fn(),
      list: vi.fn(),
      update: vi.fn(),
      delete: vi.fn(),
    } as any;
    const router = createTodoRouter(todoService);
    app = express();
    app.use(express.json());
    app.use(router);
  });

  it('GET /api/todos returns list', async () => {
    (todoService.list as any).mockResolvedValue({ todos: [], count: 0 });
    await request(app)
      .get('/api/todos')
      .expect(200)
      .expect({ todos: [], count: 0 });
  });

  it('GET /api/todos?completed=true filters', async () => {
    (todoService.list as any).mockResolvedValue({ todos: [], count: 0 });
    await request(app)
      .get('/api/todos?completed=true')
      .expect(200);
    expect(todoService.list).toHaveBeenCalledWith(true);
  });

  it('POST /api/todos creates todo', async () => {
    const newTodo = { id: '123', title: 'test', completed: false, created_at: '1', updated_at: '1' };
    (todoService.create as any).mockResolvedValue(newTodo);
    await request(app)
      .post('/api/todos')
      .send({ title: 'test' })
      .expect(201)
      .expect(newTodo);
  });

  it('POST /api/todos returns 422 for empty title', async () => {
    await request(app)
      .post('/api/todos')
      .send({ title: ' ' })
      .expect(422)
      .expect({ error: 'title_required' });
  });

  it('PUT /api/todos/:id updates todo', async () => {
    const updatedTodo = { id: '123', title: 'updated', completed: true, created_at: '1', updated_at: '2' };
    (todoService.update as any).mockResolvedValue(updatedTodo);
    await request(app)
      .put('/api/todos/123')
      .send({ title: 'updated', completed: true })
      .expect(200)
      .expect(updatedTodo);
  });

  it('PUT /api/todos/:id returns 404 not found', async () => {
    (todoService.update as any).mockRejectedValue({ error: 'todo_not_found' });
    await request(app)
      .put('/api/todos/123')
      .send({})
      .expect(404);
  });

  it('DELETE /api/todos/:id deletes', async () => {
    (todoService.delete as any).mockResolvedValue();
    await request(app)
      .delete('/api/todos/123')
      .expect(204);
  });

  it('DELETE /api/todos/:id returns 404 not found', async () => {
    (todoService.delete as any).mockRejectedValue({ error: 'todo_not_found' });
    await request(app)
      .delete('/api/todos/123')
      .expect(404);
  });
});