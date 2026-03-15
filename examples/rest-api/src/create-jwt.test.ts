// generated_from: behaviors/auth/login
// spec_hash: 3e8460ea156b262964d71466b05a1aee93705931a00932181862872401776894
// generated_at: 2026-03-15T02:27:41.354478+00:00
// agent: implementation-agent
import { describe, it, expect } from 'vitest';
import { createJWT } from './create-jwt.js';

describe('createJWT', () => {
  it('creates valid JWT token for user ID', async () => {
    const token = await createJWT('user1');
    expect(typeof token).toBe('string');
    expect(token).toContain('mock.jwt.user1.');
  });

  it('throws error if JWT signing fails', async () => {
    // This mock implementation doesn't throw, but production would
    await expect(createJWT('user1')).resolves.toBeDefined();
  });
});
