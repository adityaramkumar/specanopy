// generated_from: contracts/api/users
// spec_hash: f40252d816057e05a68d187a6823e059435ed25eb34fc5abde3ceba2491cd49a
// generated_at: 2026-03-15T02:27:22.999422+00:00
// agent: implementation-agent
export interface SignupSuccessResponse {
  id: string;
  email: string;
}

export interface SignupErrorResponse {
  error: 'invalid_email_format' | 'password_too_weak' | 'email_already_registered';
}

export type SignupResponse = SignupSuccessResponse | SignupErrorResponse;
