// generated_from: contracts/ui/components
// spec_hash: bc79e30afe2aa54205d718240aef2c47fd0990937de675688ac674d7bdae57c0
// generated_at: 2026-03-15T02:28:11.289444+00:00
// agent: testing-agent
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AddTodoForm } from './AddTodoForm';

describe('AddTodoForm', () => {
  const mockOnAdd = vi.fn();

  beforeEach(() => {
    mockOnAdd.mockClear();
  });

  it('calls onAdd with trimmed input on submit', async () => {
    render(<AddTodoForm onAdd={mockOnAdd} />);
    const input = screen.getByRole('textbox');
    const submitButton = screen.getByRole('button', { name: /add/i });

    fireEvent.change(input, { target: { value: '  Test todo  ' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnAdd).toHaveBeenCalledWith('Test todo');
    });
  });

  it('clears input after successful submit', async () => {
    render(<AddTodoForm onAdd={mockOnAdd} />);
    const input = screen.getByRole('textbox');

    fireEvent.change(input, { target: { value: 'Test todo' } });
    fireEvent.submit(input);

    await waitFor(() => {
      expect(input).toHaveValue('');
    });
  });

  it('submit button is disabled when input is empty', () => {
    render(<AddTodoForm onAdd={mockOnAdd} />);
    const submitButton = screen.getByRole('button', { name: /add/i });
    expect(submitButton).toBeDisabled();
  });

  it('submit button is disabled when input is whitespace-only', () => {
    render(<AddTodoForm onAdd={mockOnAdd} />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: '   ' } });
    const submitButton = screen.getByRole('button', { name: /add/i });
    expect(submitButton).toBeDisabled();
  });

  it('submit button is enabled when input has valid content', () => {
    render(<AddTodoForm onAdd={mockOnAdd} />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Valid todo' } });
    const submitButton = screen.getByRole('button', { name: /add/i });
    expect(submitButton).not.toBeDisabled();
  });

  it('enforces max length 200 on input field', () => {
    render(<AddTodoForm onAdd={mockOnAdd} />);
    const input = screen.getByRole('textbox');
    const longText = 'a'.repeat(201);
    fireEvent.change(input, { target: { value: longText } });
    expect(input).toHaveValue(longText.slice(0, 200));
  });
});