// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.951627+00:00
// agent: testing-agent
import { describe, it, expect, vi } from 'vitest';
import { validatePassword, PASSWORD_TOO_WEAK } from '../validate-password.js';

describe('validatePassword', () => {
  it('returns null for strong password (12+ chars, uppercase, digit, special)', () => {
    const result = validatePassword('Password123!');
    expect(result).toBeNull();
  });

  it('returns password_too_weak for password shorter than 12 characters', () => {
    const result = validatePassword('Pass123!');
    expect(result).not.toBeNull();
    expect(result?.code).toBe(PASSWORD_TOO_WEAK);
  });

  it('returns password_too_weak for password without uppercase letter', () => {
    const result = validatePassword('password123!');
    expect(result).not.toBeNull();
    expect(result?.code).toBe(PASSWORD_TOO_WEAK);
  });

  it('returns password_too_weak for password without digit', () => {
    const result = validatePassword('Password!');
    expect(result).not.toBeNull();
    expect(result?.code).toBe(PASSWORD_TOO_WEAK);
  });

  it('returns password_too_weak for password without special character', () => {
    const result = validatePassword('Password123');
    expect(result).not.toBeNull();
    expect(result?.code).toBe(PASSWORD_TOO_WEAK);
  });

  it('returns password_too_weak for empty password', () => {
    const result = validatePassword('');
    expect(result).not.toBeNull();
    expect(result?.code).toBe(PASSWORD_TOO_WEAK);
  });
});