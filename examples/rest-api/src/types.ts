// generated_from: behaviors/users/profile
// spec_hash: 0b617acb52c2f132b799bc16470845b2594558e0726d102a13875aa879178b29
// generated_at: 2026-03-15T02:28:14.740847+00:00
// agent: implementation-agent
export interface User { id: string; email: string; name: string; password_hash: string; created_at: string; }

export interface UserProfileResponse { id: string; email: string; name: string; created_at: string; }

export interface UpdateUserRequest { name: string; }

export interface ApiError { error: string; }