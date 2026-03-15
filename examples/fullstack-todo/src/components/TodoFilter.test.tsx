// generated_from: contracts/ui/components
// spec_hash: bc79e30afe2aa54205d718240aef2c47fd0990937de675688ac674d7bdae57c0
// generated_at: 2026-03-15T02:28:11.289713+00:00
// agent: testing-agent
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TodoFilter } from './TodoFilter';

describe('TodoFilter', () => {
  const mockOnChange = vi.fn();

  it.each([
    ['all', 'All'],
    ['active', 'Active'],
    ['completed', 'Completed']
  ])('renders %s button for filter=%s', (filter, buttonText) => {
    render(<TodoFilter filter={filter as any} onChange={mockOnChange} />);
    expect(screen.getByRole('button', { name: buttonText })).toBeInTheDocument();
  });

  it.each([
    ['all', 'All'],
    ['active', 'Active'],
    ['completed', 'Completed']
  ])('active $buttonText button has data-active="true" when filter=$filter', (filter, buttonText) => {
    render(<TodoFilter filter={filter as any} onChange={mockOnChange} />);
    const button = screen.getByRole('button', { name: buttonText });
    expect(button).toHaveAttribute('data-active', 'true');
  });

  it.each([
    ['all', ['Active', 'Completed']],
    ['active', ['All', 'Completed']],
    ['completed', ['All', 'Active']]
  ])('inactive buttons have data-active="false" when filter=%s', (activeFilter, inactiveButtons) => {
    render(<TodoFilter filter={activeFilter as any} onChange={mockOnChange} />);
    inactiveButtons.forEach(buttonText => {
      const button = screen.getByRole('button', { name: buttonText });
      expect(button).toHaveAttribute('data-active', 'false');
    });
  });

  it('active filter button uses bold font weight', () => {
    render(<TodoFilter filter="all" onChange={mockOnChange} />);
    const activeButton = screen.getByRole('button', { name: 'All' });
    expect(activeButton).toHaveStyle({ fontWeight: 'bold' });
  });

  it('inactive filter buttons do not use bold font weight', () => {
    render(<TodoFilter filter="all" onChange={mockOnChange} />);
    const inactiveButton = screen.getByRole('button', { name: 'Active' });
    expect(inactiveButton).not.toHaveStyle({ fontWeight: 'bold' });
  });

  it('calls onChange with correct filter when button clicked', () => {
    render(<TodoFilter filter="all" onChange={mockOnChange} />);
    fireEvent.click(screen.getByRole('button', { name: 'Active' }));
    expect(mockOnChange).toHaveBeenCalledWith('active');

    fireEvent.click(screen.getByRole('button', { name: 'Completed' }));
    expect(mockOnChange).toHaveBeenCalledWith('completed');
  });
});