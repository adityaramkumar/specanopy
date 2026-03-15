// generated_from: behaviors/backend/crud
// spec_hash: 3bc5a2b2d95a1b99ae840d8085c5ad9eb0e9da675c885ce816b5d22fbee68c88
// generated_at: 2026-03-15T02:27:52.036337+00:00
// agent: implementation-agent
import { Router } from 'express';
import type { TodoService } from '../domain/TodoService.js';
import type { Todo } from '../domain/Todo.js';
import type { ApiError } from '../domain/Todo.js';

export function createTodoRouter(todoService: TodoService): Router {
  const router = Router();

  router.get('/api/todos', async (req, res) => {
    try {
      const completed = req.query.completed === 'true' ? true : req.query.completed === 'false' ? false : null;
      const result = await todoService.list(completed);
      res.json(result);
    } catch (error) {
      res.status(500).json(error);
    }
  });

  router.post('/api/todos', async (req, res) => {
    try {
      const result = await todoService.create(req.body);
      res.status(201).json(result);
    } catch (error) {
      if ('error' in (error as ApiError)) {
        res.status(422).json(error);
      } else {
        res.status(500).json(error);
      }
    }
  });

  router.put('/api/todos/:id', async (req, res) => {
    try {
      const result = await todoService.update(req.params.id, req.body);
      res.status(200).json(result);
    } catch (error) {
      if ('error' in (error as ApiError)) {
        if ((error as ApiError).error === 'todo_not_found') {
          res.status(404).json(error);
        } else {
          res.status(422).json(error);
        }
      } else {
        res.status(500).json(error);
      }
    }
  });

  router.delete('/api/todos/:id', async (req, res) => {
    try {
      await todoService.delete(req.params.id);
      res.status(204).send();
    } catch (error) {
      if ('error' in (error as ApiError) && (error as ApiError).error === 'todo_not_found') {
        res.status(404).json(error);
      } else {
        res.status(500).json(error);
      }
    }
  });

  return router;
}
/**
 * Creates an Express router with all todo endpoints:
 * - GET /api/todos
 * - POST /api/todos
 * - PUT /api/todos/:id
 * - DELETE /api/todos/:id
 * 
 * Routes handle all validation, error responses, and HTTP status codes per spec.
 * @throws Express Error - handled internally with proper status codes
 */