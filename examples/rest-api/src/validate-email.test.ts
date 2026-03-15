// generated_from: behaviors/auth/login
// spec_hash: 3e8460ea156b262964d71466b05a1aee93705931a00932181862872401776894
// generated_at: 2026-03-15T02:27:41.337172+00:00
// agent: implementation-agent
import { describe, it, expect } from 'vitest';
import { validateEmail } from './validate-email.js';

describe('validateEmail', () => {
  it('returns valid for correct email', () => {
    const result = validateEmail('test@example.com');
    expect(result).toEqual({ isValid: true });
  });

  it('returns invalid for malformed email', () => {
    const result = validateEmail('invalid-email');
    expect(result).toEqual({ isValid: false, error: 'invalid_email_format' });
  });

  it('returns invalid for email without domain', () => {
    const result = validateEmail('test@');
    expect(result).toEqual({ isValid: false, error: 'invalid_email_format' });
  });

  it('returns invalid for email with invalid characters', () => {
    const result = validateEmail('test@@example.com');
    expect(result).toEqual({ isValid: false, error: 'invalid_email_format' });
  });
});
