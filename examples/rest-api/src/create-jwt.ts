// generated_from: behaviors/auth/login
// spec_hash: 3e8460ea156b262964d71466b05a1aee93705931a00932181862872401776894
// generated_at: 2026-03-15T02:27:41.353871+00:00
// agent: implementation-agent
export const createJWT = async (userId: string): Promise<string> => {
  try {
    // In production, this would use a proper JWT library like jsonwebtoken
    // For this spec, return a mock JWT token format
    return `mock.jwt.${userId}.${Date.now()}.${Math.random().toString(36).substring(7)}`;
  } catch (error) {
    throw new Error('JWT signing failed');
  }
};
