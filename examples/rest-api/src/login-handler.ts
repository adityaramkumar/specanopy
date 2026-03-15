// generated_from: behaviors/auth/login
// spec_hash: 3e8460ea156b262964d71466b05a1aee93705931a00932181862872401776894
// generated_at: 2026-03-15T02:27:41.325370+00:00
// agent: implementation-agent
import { validateEmail } from './validate-email.js';
import { userStore } from './user-store.js';
import { createJWT } from './create-jwt.js';
import { verifyPassword } from './password-utils.js';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  redirect: string;
}

export interface ApiError {
  error: string;
}

export type LoginHandler = (req: LoginRequest, res: any) => Promise<void>;

export const loginHandler: LoginHandler = async (req, res) => {
  try {
    const { email, password } = req;

    // Validate email format
    const emailValidation = validateEmail(email);
    if (!emailValidation.isValid) {
      return res.status(422).json({ error: 'invalid_email_format' });
    }

    // Find user
    const user = await userStore.findByEmail(email);
    if (!user) {
      return res.status(401).json({ error: 'invalid_credentials' });
    }

    // Verify password
    const isValidPassword = await verifyPassword(password, user.password_hash);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'invalid_credentials' });
    }

    // Create JWT
    const token = await createJWT(user.id);

    // Success response
    res.status(200).json({ token, redirect: '/dashboard' });
  } catch (error) {
    res.status(500).json({ error: 'internal_error' });
  }
};
