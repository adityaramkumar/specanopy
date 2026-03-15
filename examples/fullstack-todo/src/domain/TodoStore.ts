// generated_from: behaviors/backend/crud
// spec_hash: 3bc5a2b2d95a1b99ae840d8085c5ad9eb0e9da675c885ce816b5d22fbee68c88
// generated_at: 2026-03-15T02:27:52.034722+00:00
// agent: implementation-agent
import type { Todo } from './Todo.js';

export class TodoStore implements TodoStore {
  private todos: Map<string, Todo> = new Map();

  async create(todo: Todo): Promise<void> {
    this.todos.set(todo.id, todo);
  }

  async findById(id: string): Promise<Todo | null> {
    return this.todos.get(id) ?? null;
  }

  async findAll(completed?: boolean | null): Promise<Todo[]> {
    const todos = Array.from(this.todos.values());
    if (completed !== null && completed !== undefined) {
      return todos.filter(todo => todo.completed === completed);
    }
    return todos;
  }

  async update(todo: Todo): Promise<void> {
    this.todos.set(todo.id, todo);
  }

  async delete(id: string): Promise<void> {
    this.todos.delete(id);
  }
}