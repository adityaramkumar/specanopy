// generated_from: behaviors/auth/login
// spec_hash: 3e8460ea156b262964d71466b05a1aee93705931a00932181862872401776894
// generated_at: 2026-03-15T02:27:41.356021+00:00
// agent: testing-agent
import { describe, it, expect, vi } from 'vitest';
import { loginHandler } from './login-handler';
import { validateEmail } from '../validate-email';
import { userStore } from '../user-store';
import { createJWT } from '../create-jwt';
import type { LoginRequest, LoginResponse, ApiError } from './login-handler';

vi.mock('../validate-email');
vi.mock('../user-store');
vi.mock('../create-jwt');

describe('loginHandler', () => {
  const mockReq = { body: {} } as LoginRequest;
  const mockRes = {
    status: vi.fn().mockReturnThis(),
    json: vi.fn(),
    redirect: vi.fn()
  } as any;

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Happy Path', () => {
    it('should return JWT token and redirect to /dashboard for valid email and password', async () => {
      const validEmail = 'user@example.com';
      const password = 'correctpassword';
      const userId = 'user-123';
      const token = 'jwt.token.here';

      mockReq.body = { email: validEmail, password };

      (validateEmail as ReturnType<typeof vi.fn>).mockReturnValue({ isValid: true });
      (userStore.findByEmail as ReturnType<typeof vi.fn>).mockResolvedValue({
        id: userId,
        email: validEmail,
        name: 'Test User',
        password_hash: 'hashedpassword',
        created_at: '2023-01-01T00:00:00Z'
      });
      (verifyPassword as ReturnType<typeof vi.fn>).mockResolvedValue(true);
      (createJWT as ReturnType<typeof vi.fn>).mockResolvedValue(token);

      await loginHandler(mockReq, mockRes);

      expect(mockRes.status).not.toHaveBeenCalled();
      expect(mockRes.json).toHaveBeenCalledWith({ token, redirect: '/dashboard' });
      expect(mockRes.redirect).toHaveBeenCalledWith(302, '/dashboard');
    });
  });

  describe('Error Handling', () => {
    it('should return HTTP 422 with invalid_email_format for invalid email format', async () => {
      const invalidEmail = 'invalid-email';
      mockReq.body = { email: invalidEmail, password: 'password' };

      (validateEmail as ReturnType<typeof vi.fn>).mockReturnValue({
        isValid: false,
        error: 'invalid_email_format'
      });

      await loginHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(422);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'invalid_email_format' });
      expect(mockRes.redirect).not.toHaveBeenCalled();
    });

    it('should return HTTP 401 with invalid_credentials for wrong password', async () => {
      const validEmail = 'user@example.com';
      mockReq.body = { email: validEmail, password: 'wrongpassword' };

      (validateEmail as ReturnType<typeof vi.fn>).mockReturnValue({ isValid: true });
      (userStore.findByEmail as ReturnType<typeof vi.fn>).mockResolvedValue({
        id: 'user-123',
        email: validEmail,
        name: 'Test User',
        password_hash: 'hashedpassword',
        created_at: '2023-01-01T00:00:00Z'
      });
      (verifyPassword as ReturnType<typeof vi.fn>).mockResolvedValue(false);

      await loginHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(401);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'invalid_credentials' });
    });

    it('should return HTTP 500 with internal_error for unexpected error (user not found)', async () => {
      const validEmail = 'user@example.com';
      mockReq.body = { email: validEmail, password: 'password' };

      (validateEmail as ReturnType<typeof vi.fn>).mockReturnValue({ isValid: true });
      (userStore.findByEmail as ReturnType<typeof vi.fn>).mockResolvedValue(null);

      await loginHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(500);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'internal_error' });
    });

    it('should return HTTP 500 with internal_error for unexpected error (userStore throws)', async () => {
      const validEmail = 'user@example.com';
      mockReq.body = { email: validEmail, password: 'password' };

      (validateEmail as ReturnType<typeof vi.fn>).mockReturnValue({ isValid: true });
      (userStore.findByEmail as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('DB error'));

      await loginHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(500);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'internal_error' });
    });

    it('should return HTTP 500 with internal_error for unexpected error (verifyPassword throws)', async () => {
      const validEmail = 'user@example.com';
      mockReq.body = { email: validEmail, password: 'password' };

      (validateEmail as ReturnType<typeof vi.fn>).mockReturnValue({ isValid: true });
      (userStore.findByEmail as ReturnType<typeof vi.fn>).mockResolvedValue({
        id: 'user-123',
        email: validEmail,
        name: 'Test User',
        password_hash: 'hashedpassword',
        created_at: '2023-01-01T00:00:00Z'
      });
      (verifyPassword as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('Verification error'));

      await loginHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(500);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'internal_error' });
    });

    it('should return HTTP 500 with internal_error for unexpected error (createJWT throws)', async () => {
      const validEmail = 'user@example.com';
      const userId = 'user-123';
      const password = 'correctpassword';

      mockReq.body = { email: validEmail, password };

      (validateEmail as ReturnType<typeof vi.fn>).mockReturnValue({ isValid: true });
      (userStore.findByEmail as ReturnType<typeof vi.fn>).mockResolvedValue({
        id: userId,
        email: validEmail,
        name: 'Test User',
        password_hash: 'hashedpassword',
        created_at: '2023-01-01T00:00:00Z'
      });
      (verifyPassword as ReturnType<typeof vi.fn>).mockResolvedValue(true);
      (createJWT as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('JWT error'));

      await loginHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(500);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'internal_error' });
    });
  });
});