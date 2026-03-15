// generated_from: contracts/api/todos
// spec_hash: 2a5aff06c2636cc04fdde042e0308a97a8b89ba1a132aeae55374bcd169960f8
// generated_at: 2026-03-15T02:27:26.978462+00:00
// agent: testing-agent
import { describe, it, expect } from 'vitest';
import { validateTodoCreate, validateTodoUpdate, TodoError } from './todo.js';

describe('todo validation', () => {
  describe('validateTodoCreate', () => {
    it('returns null for valid title (1-200 chars)', () => {
      const result = validateTodoCreate({ title: 'Valid title' });
      expect(result).toBeNull();
    });

    it('returns title_required for empty title', () => {
      const result = validateTodoCreate({ title: '' });
      expect(result).toEqual({ error: 'title_required' });
    });

    it('returns title_required for missing title', () => {
      // @ts-expect-error testing invalid input
      const result = validateTodoCreate({});
      expect(result).toEqual({ error: 'title_required' });
    });

    it('returns title_too_long for title > 200 chars', () => {
      const longTitle = 'a'.repeat(201);
      const result = validateTodoCreate({ title: longTitle });
      expect(result).toEqual({ error: 'title_too_long' });
    });

    it('returns null for exactly 200 char title', () => {
      const validLongTitle = 'a'.repeat(200);
      const result = validateTodoCreate({ title: validLongTitle });
      expect(result).toBeNull();
    });
  });

  describe('validateTodoUpdate', () => {
    it('returns null for valid title update', () => {
      const result = validateTodoUpdate({ title: 'Valid title' });
      expect(result).toBeNull();
    });

    it('returns null for valid completed update', () => {
      const result = validateTodoUpdate({ completed: true });
      expect(result).toBeNull();
    });

    it('returns null for valid partial update', () => {
      const result = validateTodoUpdate({ title: 'Short', completed: false });
      expect(result).toBeNull();
    });

    it('returns null for empty update', () => {
      const result = validateTodoUpdate({});
      expect(result).toBeNull();
    });

    it('returns title_too_long for title > 200 chars', () => {
      const longTitle = 'a'.repeat(201);
      const result = validateTodoUpdate({ title: longTitle });
      expect(result).toEqual({ error: 'title_too_long' });
    });

    it('returns null for exactly 200 char title', () => {
      const validLongTitle = 'a'.repeat(200);
      const result = validateTodoUpdate({ title: validLongTitle });
      expect(result).toBeNull();
    });
  });
});