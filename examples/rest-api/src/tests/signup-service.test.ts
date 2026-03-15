// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.966987+00:00
// agent: testing-agent
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createSignupService, EMAIL_ALREADY_REGISTERED, INTERNAL_ERROR } from '../signup-service.js';
import type { SignupResponse } from '../user-response.js';

type UserStoreMock = {
  findByEmail: ReturnType<typeof vi.fn>;
  createUser: ReturnType<typeof vi.fn>;
};

const createMockUserStore = (): UserStoreMock => ({
  findByEmail: vi.fn(),
  createUser: vi.fn(),
});

describe('signupService', () => {
  let mockUserStore: UserStoreMock;
  let signupService: ReturnType<typeof createSignupService>;

  beforeEach(() => {
    mockUserStore = createMockUserStore();
    signupService = createSignupService(mockUserStore as any);
  });

  it('creates new user when email is not registered - happy path', async () => {
    mockUserStore.findByEmail.mockResolvedValue(null);
    mockUserStore.createUser.mockResolvedValue({ id: '123', email: 'user@example.com' } as SignupResponse);

    const result = await signupService.execute('user@example.com', 'Password123!', 'John Doe');

    expect(mockUserStore.findByEmail).toHaveBeenCalledWith('user@example.com');
    expect(mockUserStore.createUser).toHaveBeenCalledWith('user@example.com', expect.any(String), 'John Doe');
    expect(result).toEqual({ id: '123', email: 'user@example.com' });
  });

  it('throws email_already_registered when email is already registered', async () => {
    mockUserStore.findByEmail.mockResolvedValue({ id: 'existing' });

    await expect(
      signupService.execute('user@example.com', 'Password123!', 'John Doe')
    ).rejects.toMatchObject({ code: EMAIL_ALREADY_REGISTERED });

    expect(mockUserStore.findByEmail).toHaveBeenCalledWith('user@example.com');
    expect(mockUserStore.createUser).not.toHaveBeenCalled();
  });

  it('throws internal_error when user store findByEmail throws', async () => {
    mockUserStore.findByEmail.mockRejectedValue(new Error('DB error'));

    await expect(
      signupService.execute('user@example.com', 'Password123!', 'John Doe')
    ).rejects.toMatchObject({ code: INTERNAL_ERROR });
  });

  it('throws internal_error when user store createUser throws', async () => {
    mockUserStore.findByEmail.mockResolvedValue(null);
    mockUserStore.createUser.mockRejectedValue(new Error('DB error'));

    await expect(
      signupService.execute('user@example.com', 'Password123!', 'John Doe')
    ).rejects.toMatchObject({ code: INTERNAL_ERROR });
  });
});