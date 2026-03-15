// generated_from: contracts/api/todos
// spec_hash: 2a5aff06c2636cc04fdde042e0308a97a8b89ba1a132aeae55374bcd169960f8
// generated_at: 2026-03-15T02:27:26.972582+00:00
// agent: implementation-agent
export interface Todo {
  id: string;
  title: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export type TodoError = 'title_required' | 'title_too_long';

export interface ValidationError {
  error: TodoError;
}

export function validateTodoCreate(data: { title: string }): ValidationError | null {
  if (!data.title || data.title.trim().length === 0) {
    return { error: 'title_required' };
  }
  if (data.title.length > 200) {
    return { error: 'title_too_long' };
  }
  return null;
}

export function validateTodoUpdate(data: Partial<{ title: string; completed: boolean }>): ValidationError | null {
  if (data.title && data.title.length > 200) {
    return { error: 'title_too_long' };
  }
  return null;
}
