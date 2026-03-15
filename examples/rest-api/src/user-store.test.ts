// generated_from: behaviors/auth/login
// spec_hash: 3e8460ea156b262964d71466b05a1aee93705931a00932181862872401776894
// generated_at: 2026-03-15T02:27:41.352507+00:00
// agent: implementation-agent
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { userStore } from './user-store.js';

describe('userStore', () => {
  it('finds user by existing email', async () => {
    const user = await userStore.findByEmail('test@example.com');
    expect(user).toBeDefined();
    expect(user?.email).toBe('test@example.com');
  });

  it('returns null for non-existent email', async () => {
    const user = await userStore.findByEmail('nonexistent@example.com');
    expect(user).toBeNull();
  });

  it('throws error on unexpected database error', async () => {
    // Simulate database error by mocking
    const mockError = new Error('Database error');
    const originalFind = userStore.findByEmail;
    vi.spyOn(userStore, 'findByEmail').mockRejectedValueOnce(mockError);

    await expect(userStore.findByEmail('test@example.com')).rejects.toThrow('Database lookup failed');

    vi.spyOn(userStore, 'findByEmail').mockRestore();
  });
});
