// generated_from: contracts/api/users
// spec_hash: f40252d816057e05a68d187a6823e059435ed25eb34fc5abde3ceba2491cd49a
// generated_at: 2026-03-15T02:27:23.019321+00:00
// agent: testing-agent
import { describe, it, expect, vi } from 'vitest';
import { signupHandler } from './signupHandler.js';
import type { Request, Response } from 'express';
import type { SignupRequest, SignupResponse } from '../types/SignupResponse.js';

vi.mock('../types/SignupResponse.js', () => ({}));

const mockRequest = (body: SignupRequest): Request<unknown, unknown, SignupRequest> => ({
  body,
} as Request<unknown, unknown, SignupRequest>);

const mockResponse = () => {
  const res = {
    status: vi.fn().mockReturnThis(),
    json: vi.fn(),
  } as unknown as Response<SignupResponse>;
  return res;
};

describe('signupHandler', () => {
  it('POST /api/auth/signup - success (201): returns id and email', async () => {
    const req = mockRequest({
      email: 'newuser@example.com',
      password: 'StrongPass123!',
      name: 'New User',
    });
    const res = mockResponse();

    await signupHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(201);
    expect(res.json).toHaveBeenCalledWith({
      id: expect.any(String),
      email: 'newuser@example.com',
    });
  });

  it('POST /api/auth/signup - error 422: invalid_email_format', async () => {
    const req = mockRequest({
      email: 'invalid-email',
      password: 'StrongPass123!',
      name: 'User',
    });
    const res = mockResponse();

    await signupHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(422);
    expect(res.json).toHaveBeenCalledWith({
      error: 'invalid_email_format',
    });
  });

  it('POST /api/auth/signup - error 422: password_too_weak', async () => {
    const req = mockRequest({
      email: 'user@example.com',
      password: 'weak',
      name: 'User',
    });
    const res = mockResponse();

    await signupHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(422);
    expect(res.json).toHaveBeenCalledWith({
      error: 'password_too_weak',
    });
  });

  it('POST /api/auth/signup - error 409: email_already_registered', async () => {
    const req = mockRequest({
      email: 'existing@example.com',
      password: 'StrongPass123!',
      name: 'Existing User',
    });
    const res = mockResponse();

    await signupHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(409);
    expect(res.json).toHaveBeenCalledWith({
      error: 'email_already_registered',
    });
  });
});
