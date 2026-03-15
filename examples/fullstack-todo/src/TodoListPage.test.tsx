// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.729559+00:00
// agent: implementation-agent
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { TodoListPage } from './TodoListPage.js';
import * as apiClient from './api-client.js';
import * as useTodosModule from './useTodos.js';

const mockTodos = [
  { id: '1', title: 'Test Todo', completed: false, created_at: '2023-01-01T00:00:00Z', updated_at: '2023-01-01T00:00:00Z' }
];

const mockRefresh = vi.fn();
const mockAddTodo = vi.fn();
const mockToggleTodo = vi.fn();
const mockDeleteTodo = vi.fn();
const mockSetFilter = vi.fn();

const mockUseTodos = vi.fn(() => ({
  todos: mockTodos,
  filteredTodos: mockTodos,
  filter: 'all' as const,
  state: 'success',
  error: null,
  addError: null,
  refresh: mockRefresh,
  addTodo: mockAddTodo,
  toggleTodo: mockToggleTodo,
  deleteTodo: mockDeleteTodo,
  setFilter: mockSetFilter,
}));

vi.mock('./useTodos.js', () => ({ useTodos: mockUseTodos }));
vi.mock('./api-client.js');

describe('TodoListPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockUseTodos.mockReturnValue({
      todos: mockTodos,
      filteredTodos: mockTodos,
      filter: 'all' as const,
      state: 'success',
      error: null,
      addError: null,
      refresh: mockRefresh,
      addTodo: mockAddTodo,
      toggleTodo: mockToggleTodo,
      deleteTodo: mockDeleteTodo,
      setFilter: mockSetFilter,
    });
  });

  it('renders loading state', () => {
    mockUseTodos.mockReturnValue({ ...mockUseTodos(), state: 'loading' as const });
    render(<TodoListPage />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders error state with retry button', () => {
    mockUseTodos.mockReturnValue({ ...mockUseTodos(), state: 'error' as const, error: 'Failed' });
    render(<TodoListPage />);
    expect(screen.getByText('Failed to load todos. Try again.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument();
  });

  it('handles retry click', async () => {
    mockUseTodos.mockReturnValue({ ...mockUseTodos(), state: 'error' as const });
    render(<TodoListPage />);
    const retryButton = screen.getByRole('button', { name: 'Retry' });
    fireEvent.click(retryButton);
    await waitFor(() => {
      expect(mockRefresh).toHaveBeenCalled();
    });
  });

  it('renders success state with components', () => {
    render(<TodoListPage />);
    expect(screen.getByText('Test Todo')).toBeInTheDocument();
  });
});