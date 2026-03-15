// generated_from: behaviors/auth/signup
// spec_hash: f186382487e04177e71760b73b531d3b0bea1d2d470e71368e2f698403097c3a
// generated_at: 2026-03-15T02:27:56.945873+00:00
// agent: implementation-agent
export const INVALID_EMAIL_FORMAT = 'invalid_email_format' as const;

export interface ValidationError { code: string; message?: string; }

export function validateEmail(email: string): ValidationError | null {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return { code: INVALID_EMAIL_FORMAT };
  }
  return null;
}
