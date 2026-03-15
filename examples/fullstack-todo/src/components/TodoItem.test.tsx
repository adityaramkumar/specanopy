// generated_from: contracts/ui/components
// spec_hash: bc79e30afe2aa54205d718240aef2c47fd0990937de675688ac674d7bdae57c0
// generated_at: 2026-03-15T02:28:11.288799+00:00
// agent: testing-agent
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TodoItem } from './TodoItem';
import { Todo } from '../types/Todo';

describe('TodoItem', () => {
  const mockToggle = vi.fn();
  const mockDelete = vi.fn();
  const todo: Todo = {
    id: '1',
    title: 'Test todo',
    completed: false,
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-01T00:00:00Z'
  };

  it('renders checkbox checked based on todo.completed', () => {
    const incompleteTodo: Todo = { ...todo, completed: false };
    render(<TodoItem todo={incompleteTodo} onToggle={mockToggle} onDelete={mockDelete} />);
    expect(screen.getByRole('checkbox')).not.toBeChecked();

    const completeTodo: Todo = { ...todo, completed: true };
    render(<TodoItem todo={completeTodo} onToggle={mockToggle} onDelete={mockDelete} />);
    expect(screen.getByRole('checkbox')).toBeChecked();
  });

  it('renders title text', () => {
    render(<TodoItem todo={todo} onToggle={mockToggle} onDelete={mockDelete} />);
    expect(screen.getByText('Test todo')).toBeInTheDocument();
  });

  it('renders delete button', () => {
    render(<TodoItem todo={todo} onToggle={mockToggle} onDelete={mockDelete} />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('calls onToggle with todo.id when checkbox toggled', () => {
    render(<TodoItem todo={todo} onToggle={mockToggle} onDelete={mockDelete} />);
    fireEvent.click(screen.getByRole('checkbox'));
    expect(mockToggle).toHaveBeenCalledWith('1');
  });

  it('calls onDelete with todo.id when delete button clicked', () => {
    render(<TodoItem todo={todo} onToggle={mockToggle} onDelete={mockDelete} />);
    fireEvent.click(screen.getByRole('button'));
    expect(mockDelete).toHaveBeenCalledWith('1');
  });

  it('renders completed todos title with strikethrough style', () => {
    const completeTodo: Todo = { ...todo, completed: true };
    render(<TodoItem todo={completeTodo} onToggle={mockToggle} onDelete={mockDelete} />);
    const title = screen.getByText('Test todo');
    expect(title).toHaveStyle('text-decoration: line-through');
  });

  it('renders incomplete todos title without strikethrough', () => {
    render(<TodoItem todo={todo} onToggle={mockToggle} onDelete={mockDelete} />);
    const title = screen.getByText('Test todo');
    expect(title).not.toHaveStyle('text-decoration: line-through');
  });
});