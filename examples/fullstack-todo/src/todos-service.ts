// generated_from: contracts/api/todos
// spec_hash: 2a5aff06c2636cc04fdde042e0308a97a8b89ba1a132aeae55374bcd169960f8
// generated_at: 2026-03-15T02:27:26.976033+00:00
// agent: implementation-agent
import { Todo } from './todo.js';

export interface TodosService {
  getTodos(filter?: { completed?: boolean }): Promise<{ todos: Todo[]; count: number }>;
  createTodo(title: string): Promise<Todo>;
  updateTodo(id: string, data: Partial<{ title: string; completed: boolean }>): Promise<Todo | null>;
  deleteTodo(id: string): Promise<boolean>;
}
