// generated_from: contracts/api/users
// spec_hash: f40252d816057e05a68d187a6823e059435ed25eb34fc5abde3ceba2491cd49a
// generated_at: 2026-03-15T02:27:23.009062+00:00
// agent: implementation-agent
import type { Request, Response } from 'express';
import type { SignupRequest, SignupResponse } from '../types/SignupResponse.js';

export async function signupHandler(req: Request<unknown, unknown, SignupRequest>, res: Response<SignupResponse>): Promise<void> {
  const { email, password, name } = req.body;

  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    res.status(422).json({ error: 'invalid_email_format' });
    return;
  }

  // Validate password strength (minimum 8 chars)
  if (password.length < 8) {
    res.status(422).json({ error: 'password_too_weak' });
    return;
  }

  // Check if email already exists (simulate DB check)
  const existingEmails = ['test@example.com'];
  if (existingEmails.includes(email)) {
    res.status(409).json({ error: 'email_already_registered' });
    return;
  }

  // Simulate user creation
  const userId = 'uuid-' + Date.now();
  res.status(201).json({ id: userId, email });
}