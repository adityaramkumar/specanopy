// generated_from: behaviors/users/profile
// spec_hash: 0b617acb52c2f132b799bc16470845b2594558e0726d102a13875aa879178b29
// generated_at: 2026-03-15T02:28:14.748655+00:00
// agent: implementation-agent
import type { User } from './types.js';

interface UserStore {
  getUserById(id: string): User | undefined;
  updateUser(id: string, updates: Partial<User>): User;
}

const users: Map<string, User> = new Map();

export const usersStore: UserStore = {
  getUserById(id: string): User | undefined {
    return users.get(id);
  },

  updateUser(id: string, updates: Partial<User>): User {
    const user = users.get(id);
    if (!user) {
      throw new Error('User not found');
    }
    const updatedUser = { ...user, ...updates };
    users.set(id, updatedUser);
    return updatedUser;
  }
};

export function initializeUsersStore(): void {
  users.clear();
}

export function resetUsersStore(): void {
  users.clear();
}