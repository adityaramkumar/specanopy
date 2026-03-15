// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.967907+00:00
// agent: testing-agent
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createSignupHandler } from '../signup-handler.js';
import type { SignupResponse } from '../user-response.js';

type SignupServiceMock = {
  execute: ReturnType<typeof vi.fn>;
};

const createMockSignupService = (): SignupServiceMock => ({
  execute: vi.fn(),
});

describe('signupHandler', () => {
  let mockSignupService: SignupServiceMock;
  let handler: ReturnType<typeof createSignupHandler>;

  beforeEach(() => {
    mockSignupService = createMockSignupService();
    handler = createSignupHandler(mockSignupService as any);
  });

  it('returns HTTP 201 with user data on successful signup - happy path', async () => {
    const signupResponse: SignupResponse = { id: '123', email: 'user@example.com' };
    mockSignupService.execute.mockResolvedValue(signupResponse);

    const result = await handler.handle({
      email: 'user@example.com',
      password: 'Password123!',
      name: 'John Doe',
    });

    expect(result.status).toBe(201);
    expect(result.body).toEqual(signupResponse);
    expect(mockSignupService.execute).toHaveBeenCalledWith(
      'user@example.com',
      'Password123!',
      'John Doe'
    );
  });

  it('returns HTTP 422 with invalid_email_format when validation fails', async () => {
    mockSignupService.execute.mockRejectedValue({ code: 'invalid_email_format' });

    const result = await handler.handle({
      email: 'invalid',
      password: 'Password123!',
      name: 'John Doe',
    });

    expect(result.status).toBe(422);
    expect(result.body).toEqual({ error: 'invalid_email_format' });
  });

  it('returns HTTP 422 with password_too_weak when validation fails', async () => {
    mockSignupService.execute.mockRejectedValue({ code: 'password_too_weak' });

    const result = await handler.handle({
      email: 'user@example.com',
      password: 'weak',
      name: 'John Doe',
    });

    expect(result.status).toBe(422);
    expect(result.body).toEqual({ error: 'password_too_weak' });
  });

  it('returns HTTP 409 with email_already_registered when email exists', async () => {
    mockSignupService.execute.mockRejectedValue({ code: 'email_already_registered' });

    const result = await handler.handle({
      email: 'existing@example.com',
      password: 'Password123!',
      name: 'John Doe',
    });

    expect(result.status).toBe(409);
    expect(result.body).toEqual({ error: 'email_already_registered' });
  });

  it('returns HTTP 500 with internal_error for unexpected errors', async () => {
    mockSignupService.execute.mockRejectedValue(new Error('Unexpected error'));

    const result = await handler.handle({
      email: 'user@example.com',
      password: 'Password123!',
      name: 'John Doe',
    });

    expect(result.status).toBe(500);
    expect(result.body).toEqual({ error: 'internal_error' });
  });
});