// generated_from: behaviors/backend/crud
// spec_hash: 3bc5a2b2d95a1b99ae840d8085c5ad9eb0e9da675c885ce816b5d22fbee68c88
// generated_at: 2026-03-15T02:27:52.034232+00:00
// agent: implementation-agent
import type { Todo, TodoListResponse, ApiError } from './Todo.js';
import type { UuidAdapter } from '../adapters/UuidAdapter.js';
import type { DateAdapter } from '../adapters/DateAdapter.js';
import type { TodoStore } from './TodoStore.js';

export interface CreateTodoInput {
  title: string;
}

export interface UpdateTodoInput {
  title?: string;
  completed?: boolean;
}

export class TodoService {
  constructor(
    private uuidAdapter: UuidAdapter,
    private dateAdapter: DateAdapter,
    private todoStore: TodoStore
  ) {}

  async create(input: CreateTodoInput): Promise<Todo> {
    const titleTrimmed = input.title.trim();
    if (titleTrimmed.length === 0) {
      throw { error: 'title_required' } as ApiError;
    }
    if (titleTrimmed.length > 200) {
      throw { error: 'title_too_long' } as ApiError;
    }

    const now = this.dateAdapter.nowIso();
    const todo: Todo = {
      id: this.uuidAdapter.generate(),
      title: titleTrimmed,
      completed: false,
      created_at: now,
      updated_at: now,
    };

    await this.todoStore.create(todo);
    return todo;
  }

  /**
   * @throws ApiError - title_required if title is empty or whitespace only
   * @throws ApiError - title_too_long if title exceeds 200 characters
   */
  async list(completed?: boolean | null): Promise<TodoListResponse> {
    const todos = await this.todoStore.findAll(completed);
    return {
      todos: todos.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()),
      count: todos.length,
    };
  }

  async update(id: string, input: UpdateTodoInput): Promise<Todo> {
    const existing = await this.todoStore.findById(id);
    if (!existing) {
      throw { error: 'todo_not_found' } as ApiError;
    }

    let title = existing.title;
    if (input.title !== undefined) {
      const titleTrimmed = input.title.trim();
      if (titleTrimmed.length > 200) {
        throw { error: 'title_too_long' } as ApiError;
      }
      title = titleTrimmed;
    }

    const updatedTodo: Todo = {
      ...existing,
      title,
      completed: input.completed ?? existing.completed,
      updated_at: this.dateAdapter.nowIso(),
    };

    await this.todoStore.update(updatedTodo);
    return updatedTodo;
  }

  /**
   * @throws ApiError - todo_not_found if todo doesn't exist
   * @throws ApiError - title_too_long if title exceeds 200 characters
   */

  async delete(id: string): Promise<void> {
    const existing = await this.todoStore.findById(id);
    if (!existing) {
      throw { error: 'todo_not_found' } as ApiError;
    }
    await this.todoStore.delete(id);
  }

  /** @throws ApiError - todo_not_found if todo doesn't exist */
}