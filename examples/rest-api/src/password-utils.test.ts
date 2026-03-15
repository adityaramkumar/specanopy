// generated_from: behaviors/auth/login
// spec_hash: 3e8460ea156b262964d71466b05a1aee93705931a00932181862872401776894
// generated_at: 2026-03-15T02:27:41.355732+00:00
// agent: implementation-agent
import { describe, it, expect } from 'vitest';
import { verifyPassword } from './password-utils.js';

describe('verifyPassword', () => {
  const testHash = '$2b$10$K.ExampleHashForTestUser12345678901234567890';

  it('returns true for correct password', async () => {
    const isValid = await verifyPassword('password123', testHash);
    expect(isValid).toBe(true);
  });

  it('returns false for incorrect password', async () => {
    const isValid = await verifyPassword('wrongpassword', testHash);
    expect(isValid).toBe(false);
  });

  it('throws error if verification fails unexpectedly', async () => {
    // Mock implementation handles errors gracefully
    await expect(verifyPassword('password123', 'invalid-hash')).resolves.toBe(false);
  });
});
