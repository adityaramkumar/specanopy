// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.950384+00:00
// agent: implementation-agent
import { describe, it, expect, vi } from 'vitest';
import { validateEmail, INVALID_EMAIL_FORMAT } from './validate-email.js';
import { validatePassword, PASSWORD_TOO_WEAK } from './validate-password.js';
import { createSignupHandler } from './signup-handler.js';
import { createSignupService } from './signup-service.js';

describe('Signup Behavior', () => {
  describe('validateEmail', () => {
    it('returns null for valid email', () => {
      expect(validateEmail('test@example.com')).toBeNull();
    });

    it('returns error for invalid email format', () => {
      const result = validateEmail('invalid-email');
      expect(result).not.toBeNull();
      expect(result?.code).toBe(INVALID_EMAIL_FORMAT);
    });
  });

  describe('validatePassword', () => {
    it('returns null for strong password', () => {
      expect(validatePassword('Password123!')).toBeNull();
    });

    it('returns error for password too short', () => {
      const result = validatePassword('short');
      expect(result).not.toBeNull();
      expect(result?.code).toBe(PASSWORD_TOO_WEAK);
    });

    it('returns error for no uppercase', () => {
      const result = validatePassword('password123!abcdefghijklm');
      expect(result).not.toBeNull();
      expect(result?.code).toBe(PASSWORD_TOO_WEAK);
    });

    it('returns error for no digit', () => {
      const result = validatePassword('Passwordabcdefghijklm!');
      expect(result).not.toBeNull();
      expect(result?.code).toBe(PASSWORD_TOO_WEAK);
    });

    it('returns error for no special character', () => {
      const result = validatePassword('Password123abcdefghijklm');
      expect(result).not.toBeNull();
      expect(result?.code).toBe(PASSWORD_TOO_WEAK);
    });
  });

  describe('signup handler', () => {
    it('returns 201 with user data on success', async () => {
      const mockUserStore = {
        findByEmail: vi.fn().mockResolvedValue(null),
        createUser: vi.fn().mockResolvedValue({
          id: 'user-123',
          email: 'test@example.com',
        }),
      };

      const signupService = createSignupService(mockUserStore);
      const handler = createSignupHandler(signupService);

      const result = await handler.handle({
        email: 'test@example.com',
        password: 'Password123!',
        name: 'Test User',
      });

      expect(result.status).toBe(201);
      expect(result.body).toEqual({
        id: 'user-123',
        email: 'test@example.com',
      });
    });

    it('returns 422 for invalid email format', async () => {
      const signupService = createSignupService({} as any);
      const handler = createSignupHandler(signupService);

      const result = await handler.handle({
        email: 'invalid-email',
        password: 'Password123!',
        name: 'Test User',
      });

      expect(result.status).toBe(422);
      expect(result.body).toEqual({ error: INVALID_EMAIL_FORMAT });
    });

    it('returns 422 for weak password', async () => {
      const signupService = createSignupService({} as any);
      const handler = createSignupHandler(signupService);

      const result = await handler.handle({
        email: 'test@example.com',
        password: 'weak',
        name: 'Test User',
      });

      expect(result.status).toBe(422);
      expect(result.body).toEqual({ error: PASSWORD_TOO_WEAK });
    });

    it('returns 409 for email already registered', async () => {
      const mockUserStore = {
        findByEmail: vi.fn().mockResolvedValue({ id: 'existing' }),
        createUser: vi.fn(),
      };

      const signupService = createSignupService(mockUserStore);
      const handler = createSignupHandler(signupService);

      const result = await handler.handle({
        email: 'test@example.com',
        password: 'Password123!',
        name: 'Test User',
      });

      expect(result.status).toBe(409);
      expect(result.body).toEqual({ error: 'email_already_registered' });
    });

    it('returns 500 for internal errors', async () => {
      const mockUserStore = {
        findByEmail: vi.fn().mockRejectedValue(new Error('db error')),
        createUser: vi.fn(),
      };

      const signupService = createSignupService(mockUserStore);
      const handler = createSignupHandler(signupService);

      const result = await handler.handle({
        email: 'test@example.com',
        password: 'Password123!',
        name: 'Test User',
      });

      expect(result.status).toBe(500);
      expect(result.body).toEqual({ error: 'internal_error' });
    });
  });
});
