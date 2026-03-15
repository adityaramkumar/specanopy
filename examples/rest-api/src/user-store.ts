// generated_from: behaviors/auth/login
// spec_hash: 3e8460ea156b262964d71466b05a1aee93705931a00932181862872401776894
// generated_at: 2026-03-15T02:27:41.351429+00:00
// agent: implementation-agent
export interface User {
  id: string;
  email: string;
  name: string;
  password_hash: string;
  created_at: string;
}

export interface UserStore {
  findByEmail(email: string): Promise<User | null>;
}

const users: User[] = [
  {
    id: 'user1',
    email: 'test@example.com',
    name: 'Test User',
    password_hash: '$2b$10$K.ExampleHashForTestUser12345678901234567890',
    created_at: '2023-01-01T00:00:00Z'
  }
];

export const userStore: UserStore = {
  async findByEmail(email: string): Promise<User | null> {
    try {
      return users.find(user => user.email === email) || null;
    } catch (error) {
      throw new Error('Database lookup failed');
    }
  }
};
