// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.724895+00:00
// agent: implementation-agent
export interface Todo { id: string; title: string; completed: boolean; created_at: string; updated_at: string; }

export interface ApiResponse<T> { data: T; }

export interface TodosResponse { todos: Todo[]; count: number; }

export type ApiError = { error: string; };

export type Filter = 'all' | 'active' | 'completed';

export type TodosState = 'loading' | 'error' | 'success';

export interface TodoActionLock { id: string; type: 'toggle' | 'delete'; pending: boolean; }