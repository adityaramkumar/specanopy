// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.951054+00:00
// agent: testing-agent
import { describe, it, expect, vi } from 'vitest';
import { validateEmail, INVALID_EMAIL_FORMAT } from '../validate-email.js';

describe('validateEmail', () => {
  it('returns null for valid email format', () => {
    const result = validateEmail('user@example.com');
    expect(result).toBeNull();
  });

  it('returns ValidationError with invalid_email_format for invalid email', () => {
    const result = validateEmail('invalid-email');
    expect(result).not.toBeNull();
    expect(result?.code).toBe(INVALID_EMAIL_FORMAT);
  });

  it('returns ValidationError with invalid_email_format for empty email', () => {
    const result = validateEmail('');
    expect(result).not.toBeNull();
    expect(result?.code).toBe(INVALID_EMAIL_FORMAT);
  });

  it('returns ValidationError with invalid_email_format for email without domain', () => {
    const result = validateEmail('user@');
    expect(result).not.toBeNull();
    expect(result?.code).toBe(INVALID_EMAIL_FORMAT);
  });
});