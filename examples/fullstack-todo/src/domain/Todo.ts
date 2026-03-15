// generated_from: behaviors/backend/crud
// spec_hash: 3bc5a2b2d95a1b99ae840d8085c5ad9eb0e9da675c885ce816b5d22fbee68c88
// generated_at: 2026-03-15T02:27:52.032492+00:00
// agent: implementation-agent
export interface Todo {
  id: string;
  title: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TodoListResponse {
  todos: Todo[];
  count: number;
}

export interface ApiError {
  error: string;
}