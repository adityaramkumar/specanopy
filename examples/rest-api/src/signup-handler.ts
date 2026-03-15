// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.949568+00:00
// agent: implementation-agent
import { validateEmail, INVALID_EMAIL_FORMAT } from './validate-email.js';
import { validatePassword, PASSWORD_TOO_WEAK } from './validate-password.js';
import type { SignupResponse } from './user-response.js';

export interface SignupRequestHandler {
  handle(request: {
    email: string;
    password: string;
    name: string;
  }): Promise<{
    status: number;
    body: SignupResponse | { error: string };
  }>;
}

export function createSignupHandler(signupService: {
  execute(email: string, password: string, name: string): Promise<SignupResponse>;
}): SignupRequestHandler {
  return {
    async handle(request: {
      email: string;
      password: string;
      name: string;
    }): Promise<{
      status: number;
      body: SignupResponse | { error: string };
    }> {
      const { email, password, name } = request;

      const emailError = validateEmail(email);
      if (emailError) {
        return {
          status: 422,
          body: { error: emailError.code },
        };
      }

      const passwordError = validatePassword(password);
      if (passwordError) {
        return {
          status: 422,
          body: { error: passwordError.code },
        };
      }

      try {
        const user = await signupService.execute(email, password, name);
        return {
          status: 201,
          body: user,
        };
      } catch (error) {
        if (error instanceof Error) {
          if (error.message === 'email_already_registered') {
            return {
              status: 409,
              body: { error: 'email_already_registered' },
            };
          }
          if (error.message === 'internal_error') {
            return {
              status: 500,
              body: { error: 'internal_error' },
            };
          }
        }
        return {
          status: 500,
          body: { error: 'internal_error' },
        };
      }
    },
  };
}
