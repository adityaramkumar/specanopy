// generated_from: behaviors/users/profile
// spec_hash: 0b617acb52c2f132b799bc16470845b2594558e0726d102a13875aa879178b29
// generated_at: 2026-03-15T02:28:14.753836+00:00
// agent: implementation-agent
import { describe, it, expect, beforeEach } from 'vitest';

import { UserService } from './userService.js';

import { usersStore, initializeUsersStore, resetUsersStore } from './inMemoryUsers.js';

import type { User } from './types.js';

describe('UserService', () => {
  beforeEach(() => {
    resetUsersStore();
  });

  describe('getUserProfile', () => {
    it('returns user profile when user exists', () => {
      const mockUser: User = {
        id: '123',
        email: 'test@example.com',
        name: 'Test User',
        password_hash: 'hashed',
        created_at: '2023-01-01T00:00:00Z'
      };
      usersStore.updateUser('123', mockUser);

      const service = new UserService(usersStore);
      const result = service.getUserProfile('123');

      expect(result).toEqual({
        id: '123',
        email: 'test@example.com',
        name: 'Test User',
        created_at: '2023-01-01T00:00:00Z'
      });
    });

    it('returns user_not_found error when user does not exist', () => {
      const service = new UserService(usersStore);
      const result = service.getUserProfile('nonexistent');

      expect(result).toEqual({ error: 'user_not_found' });
    });
  });

  describe('updateUserProfile', () => {
    it('updates user name successfully', () => {
      const mockUser: User = {
        id: '123',
        email: 'test@example.com',
        name: 'Old Name',
        password_hash: 'hashed',
        created_at: '2023-01-01T00:00:00Z'
      };
      usersStore.updateUser('123', mockUser);

      const service = new UserService(usersStore);
      const result = service.updateUserProfile('123', { name: 'New Name' });

      expect(result).toEqual({
        id: '123',
        email: 'test@example.com',
        name: 'New Name',
        created_at: '2023-01-01T00:00:00Z'
      });
    });

    it('returns name_required error for empty name', () => {
      const service = new UserService(usersStore);
      const result = service.updateUserProfile('123', { name: '' });

      expect(result).toEqual({ error: 'name_required' });
    });

    it('returns name_required error for missing name', () => {
      const service = new UserService(usersStore);
      // @ts-expect-error Testing invalid input
      const result = service.updateUserProfile('123', { });

      expect(result).toEqual({ error: 'name_required' });
    });

    it('returns name_too_long error for name longer than 100 chars', () => {
      const longName = 'a'.repeat(101);
      const service = new UserService(usersStore);
      const result = service.updateUserProfile('123', { name: longName });

      expect(result).toEqual({ error: 'name_too_long' });
    });

    it('trims whitespace from name', () => {
      const mockUser: User = {
        id: '123',
        email: 'test@example.com',
        name: 'Old Name',
        password_hash: 'hashed',
        created_at: '2023-01-01T00:00:00Z'
      };
      usersStore.updateUser('123', mockUser);

      const service = new UserService(usersStore);
      const result = service.updateUserProfile('123', { name: '  New Name  ' });

      expect(result?.name).toBe('New Name');
    });
  });
});