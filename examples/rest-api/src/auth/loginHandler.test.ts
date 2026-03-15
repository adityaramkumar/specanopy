// generated_from: contracts/api/users
// spec_hash: f40252d816057e05a68d187a6823e059435ed25eb34fc5abde3ceba2491cd49a
// generated_at: 2026-03-15T02:27:23.015882+00:00
// agent: testing-agent
import { describe, it, expect, vi } from 'vitest';
import { loginHandler } from './loginHandler.js';
import type { Request, Response } from 'express';
import type { LoginRequest, LoginResponse } from '../types/LoginResponse.js';

vi.mock('../types/LoginResponse.js', () => ({}));

const mockRequest = (body: LoginRequest): Request<unknown, unknown, LoginRequest> => ({
  body,
} as Request<unknown, unknown, LoginRequest>);

const mockResponse = () => {
  const res = {
    status: vi.fn().mockReturnThis(),
    json: vi.fn(),
    redirect: vi.fn(),
  } as unknown as Response<LoginResponse>;
  return res;
};

describe('loginHandler', () => {
  it('POST /api/auth/login - success (200): returns token and redirect', async () => {
    const req = mockRequest({ email: 'user@example.com', password: 'correctpass' });
    const res = mockResponse();

    await loginHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(200);
    expect(res.json).toHaveBeenCalledWith({
      token: expect.any(String),
      redirect: '/dashboard',
    });
  });

  it('POST /api/auth/login - error 422: invalid_email_format', async () => {
    const req = mockRequest({ email: 'invalid-email', password: 'password' });
    const res = mockResponse();

    await loginHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(422);
    expect(res.json).toHaveBeenCalledWith({
      error: 'invalid_email_format',
    });
  });

  it('POST /api/auth/login - error 401: invalid_credentials', async () => {
    const req = mockRequest({ email: 'user@example.com', password: 'wrongpass' });
    const res = mockResponse();

    await loginHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json).toHaveBeenCalledWith({
      error: 'invalid_credentials',
    });
  });
});
