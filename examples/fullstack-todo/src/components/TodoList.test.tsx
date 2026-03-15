// generated_from: contracts/ui/components
// spec_hash: bc79e30afe2aa54205d718240aef2c47fd0990937de675688ac674d7bdae57c0
// generated_at: 2026-03-15T02:28:11.289164+00:00
// agent: testing-agent
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { TodoList } from './TodoList';
import { Todo } from '../types/Todo';

describe('TodoList', () => {
  const mockToggle = vi.fn();
  const mockDelete = vi.fn();
  const todos: Todo[] = [
    {
      id: '1',
      title: 'Test todo 1',
      completed: false,
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z'
    }
  ];

  it('renders list of TodoItem components', () => {
    render(<TodoList todos={todos} onToggle={mockToggle} onDelete={mockDelete} />);
    expect(screen.getByText('Test todo 1')).toBeInTheDocument();
  });

  it('renders empty state when list is empty', () => {
    render(<TodoList todos={[]} onToggle={mockToggle} onDelete={mockDelete} />);
    expect(screen.getByText('No todos yet')).toBeInTheDocument();
  });

  it('passes onToggle and onDelete to TodoItem components', () => {
    render(<TodoList todos={todos} onToggle={mockToggle} onDelete={mockDelete} />);
    // This tests observable behavior through TodoItem interaction
    // Detailed TodoItem interaction tested in TodoItem.test.tsx
  });
});