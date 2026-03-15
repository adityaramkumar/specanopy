// generated_from: behaviors/users/profile
// spec_hash: 0b617acb52c2f132b799bc16470845b2594558e0726d102a13875aa879178b29
// generated_at: 2026-03-15T02:28:14.752104+00:00
// agent: implementation-agent
import type { User, UserProfileResponse, UpdateUserRequest, ApiError } from './types.js';

import type { UserStore } from './inMemoryUsers.js';

export class UserService {
  constructor(private usersStore: UserStore) {}

  getUserProfile(id: string): UserProfileResponse | ApiError {
    const user = this.usersStore.getUserById(id);
    if (!user) {
      return { error: 'user_not_found' };
    }
    const { id: userId, email, name, created_at } = user;
    return { id: userId, email, name, created_at };
  }

  updateUserProfile(id: string, data: UpdateUserRequest): UserProfileResponse | ApiError {
    if (!data.name || data.name.trim() === '') {
      return { error: 'name_required' };
    }

    if (data.name.length > 100) {
      return { error: 'name_too_long' };
    }

    try {
      const updatedUser = this.usersStore.updateUser(id, { name: data.name });
      const { id: userId, email, name, created_at } = updatedUser;
      return { id: userId, email, name, created_at };
    } catch {
      return { error: 'user_not_found' };
    }
  }
}