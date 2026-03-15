// generated_from: contracts/api/todos
// spec_hash: 2a5aff06c2636cc04fdde042e0308a97a8b89ba1a132aeae55374bcd169960f8
// generated_at: 2026-03-15T02:27:26.973973+00:00
// agent: implementation-agent
import { Router } from 'express';
import { TodosService } from './todos-service.js';
import type { Todo, ValidationError } from './todo.js';

export function createTodosRouter(service: TodosService): Router {
  const router = Router({ mergeParams: true });

  // GET /api/todos?completed=true|false
  router.get('/todos', async (req, res) => {
    const filter = req.query.completed ? { completed: req.query.completed === 'true' } : undefined;
    const result = await service.getTodos(filter);
    res.json(result);
  });

  // POST /api/todos
  router.post('/todos', async (req, res) => {
    const validation = validateTodoCreate(req.body);
    if (validation) {
      return res.status(422).json(validation);
    }
    try {
      const todo = await service.createTodo(req.body.title);
      res.status(201).json(todo);
    } catch (error) {
      // Service throws validation errors
      if ((error as any).error) {
        return res.status(422).json(error);
      }
      throw error;
    }
  });

  // PUT /api/todos/:id
  router.put('/todos/:id', async (req, res) => {
    const validation = validateTodoUpdate(req.body);
    if (validation) {
      return res.status(422).json(validation);
    }

    const todo = await service.updateTodo(req.params.id, req.body);
    if (!todo) {
      return res.status(404).json({ error: 'todo_not_found' });
    }
    res.json(todo);
  });

  // DELETE /api/todos/:id
  router.delete('/todos/:id', async (req, res) => {
    const deleted = await service.deleteTodo(req.params.id);
    if (!deleted) {
      return res.status(404).json({ error: 'todo_not_found' });
    }
    res.status(204).send();
  });

  return router;
}
