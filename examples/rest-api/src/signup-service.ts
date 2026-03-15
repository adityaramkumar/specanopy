// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.948826+00:00
// agent: implementation-agent
import type { SignupResponse } from './user-response.js';

export const EMAIL_ALREADY_REGISTERED = 'email_already_registered' as const;
export const INTERNAL_ERROR = 'internal_error' as const;

export interface UserStore {
  findByEmail(email: string): Promise<{ id: string } | null>;
  createUser(email: string, passwordHash: string, name: string): Promise<SignupResponse>;
}

export interface SignupService {
  execute(email: string, password: string, name: string): Promise<SignupResponse>;
}

export function createSignupService(userStore: UserStore): SignupService {
  return {
    async execute(email: string, password: string, name: string): Promise<SignupResponse> {
      try {
        const existingUser = await userStore.findByEmail(email);
        if (existingUser) {
          throw new Error(EMAIL_ALREADY_REGISTERED);
        }

        // Simple hash simulation - in production use bcrypt/argon2
        const passwordHash = `hashed_${password}`;

        return await userStore.createUser(email, passwordHash, name);
      } catch (error) {
        if (error instanceof Error && error.message === EMAIL_ALREADY_REGISTERED) {
          throw new Error(EMAIL_ALREADY_REGISTERED);
        }
        throw new Error(INTERNAL_ERROR);
      }
    },
  };
}
