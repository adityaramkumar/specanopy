// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.946912+00:00
// agent: implementation-agent
export const PASSWORD_TOO_WEAK = 'password_too_weak' as const;

export interface ValidationError { code: string; message?: string; }

export function validatePassword(password: string): ValidationError | null {
  if (password.length < 12) {
    return { code: PASSWORD_TOO_WEAK };
  }
  if (!/[A-Z]/.test(password)) {
    return { code: PASSWORD_TOO_WEAK };
  }
  if (!/[0-9]/.test(password)) {
    return { code: PASSWORD_TOO_WEAK };
  }
  if (!/[^A-Za-z0-9]/.test(password)) {
    return { code: PASSWORD_TOO_WEAK };
  }
  return null;
}
