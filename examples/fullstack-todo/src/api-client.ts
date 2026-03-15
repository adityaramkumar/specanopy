// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.726722+00:00
// agent: implementation-agent
const API_BASE = '/api';

export async function fetchTodos(): Promise<TodosResponse> {
  const response = await fetch(`${API_BASE}/todos`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

export async function createTodo(title: string): Promise<Todo> {
  const response = await fetch(`${API_BASE}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

export async function updateTodo(id: string, updates: { completed?: boolean; title?: string }): Promise<Todo> {
  const response = await fetch(`${API_BASE}/todos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates),
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

export async function deleteTodo(id: string): Promise<void> {
  const response = await fetch(`${API_BASE}/todos/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }
}