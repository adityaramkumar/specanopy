// generated_from: behaviors/frontend/todo-list
// spec_hash: 8fefe85bf4a95c7a13aaf8dfd2ea65a14a2294e1e908e4282124800ad72d2b5b
// generated_at: 2026-03-15T02:28:34.732218+00:00
// agent: testing-agent
// TodoListPage.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { TodoListPage } from '../TodoListPage';
import { useTodos } from '../useTodos';

vi.mock('../useTodos');

const mockUseTodos = useTodos as any;

describe('TodoListPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state on mount', () => {
    mockUseTodos.mockReturnValue({
      state: 'loading',
      todos: [],
      filteredTodos: [],
      filter: 'all' as any,
      error: null,
      addError: null,
      refresh: vi.fn(),
      addTodo: vi.fn(),
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      setFilter: vi.fn()
    });

    render(<TodoListPage />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders error state with retry button', () => {
    mockUseTodos.mockReturnValue({
      state: 'error',
      todos: [],
      filteredTodos: [],
      filter: 'all' as any,
      error: 'Failed to load',
      addError: null,
      refresh: vi.fn(),
      addTodo: vi.fn(),
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      setFilter: vi.fn()
    });

    render(<TodoListPage />);
    expect(screen.getByText('Failed to load todos. Try again.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
  });

  it('retry button calls refresh without page reload', async () => {
    const mockRefresh = vi.fn();
    mockUseTodos.mockReturnValue({
      state: 'error',
      todos: [],
      filteredTodos: [],
      filter: 'all' as any,
      error: 'Failed to load',
      addError: null,
      refresh: mockRefresh,
      addTodo: vi.fn(),
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      setFilter: vi.fn()
    });

    render(<TodoListPage />);
    fireEvent.click(screen.getByRole('button', { name: /retry/i }));

    expect(mockRefresh).toHaveBeenCalledTimes(1);
  });

  it('renders success state with todo list', () => {
    mockUseTodos.mockReturnValue({
      state: 'success',
      todos: [],
      filteredTodos: [],
      filter: 'all' as any,
      error: null,
      addError: null,
      refresh: vi.fn(),
      addTodo: vi.fn(),
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      setFilter: vi.fn()
    });

    render(<TodoListPage />);
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    expect(screen.queryByText('Failed to load todos. Try again.')).not.toBeInTheDocument();
  });

  it('shows add todo error message after failed add attempt', () => {
    mockUseTodos.mockReturnValue({
      state: 'success',
      todos: [],
      filteredTodos: [],
      filter: 'all' as any,
      error: null,
      addError: 'Failed to add todo',
      refresh: vi.fn(),
      addTodo: vi.fn(),
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      setFilter: vi.fn()
    });

    render(<TodoListPage />);
    expect(screen.getByText('Failed to add todo')).toBeInTheDocument();
  });

  it('renders TodoFilter component with correct active states', () => {
    mockUseTodos.mockReturnValue({
      state: 'success',
      todos: [],
      filteredTodos: [],
      filter: 'active' as any,
      error: null,
      addError: null,
      refresh: vi.fn(),
      addTodo: vi.fn(),
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      setFilter: vi.fn()
    });

    render(<TodoListPage />);

    const activeButton = screen.getByRole('button', { name: /active/i });
    expect(activeButton).toHaveAttribute('data-active', 'true');

    const allButton = screen.getByRole('button', { name: /all/i });
    expect(allButton).toHaveAttribute('data-active', 'false');
  });

  it('renders AddTodoForm and handles submission', async () => {
    const mockAddTodo = vi.fn();
    mockUseTodos.mockReturnValue({
      state: 'success',
      todos: [],
      filteredTodos: [],
      filter: 'all' as any,
      error: null,
      addError: null,
      refresh: vi.fn(),
      addTodo: mockAddTodo,
      toggleTodo: vi.fn(),
      deleteTodo: vi.fn(),
      setFilter: vi.fn()
    });

    render(<TodoListPage />);

    const input = screen.getByRole('textbox');
    const form = input.closest('form')!;

    fireEvent.change(input, { target: { value: 'New Todo' } });
    fireEvent.submit(form);

    await waitFor(() => {
      expect(mockAddTodo).toHaveBeenCalledWith('New Todo');
    });
  });
});