// generated_from: contracts/api/users
// spec_hash: f40252d816057e05a68d187a6823e059435ed25eb34fc5abde3ceba2491cd49a
// generated_at: 2026-03-15T02:27:23.002754+00:00
// agent: implementation-agent
import type { Request, Response } from 'express';
import type { LoginRequest, LoginResponse } from '../types/LoginResponse.js';

export async function loginHandler(req: Request<unknown, unknown, LoginRequest>, res: Response<LoginResponse>): Promise<void> {
  const { email, password } = req.body;

  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    res.status(422).json({ error: 'invalid_email_format' });
    return;
  }

  // Simulate credential validation (replace with real DB/auth logic)
  if (email !== 'test@example.com' || password !== 'password123') {
    res.status(401).json({ error: 'invalid_credentials' });
    return;
  }

  res.status(200).json({ token: 'mock-jwt-token', redirect: '/dashboard' });
}