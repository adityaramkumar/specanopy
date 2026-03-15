// generated_from: behaviors/users/profile
// spec_hash: 0b617acb52c2f132b799bc16470845b2594558e0726d102a13875aa879178b29
// generated_at: 2026-03-15T02:28:14.757103+00:00
// agent: testing-agent
// no types or store imports - test observable behavior only
import { describe, it, expect, beforeEach } from 'vitest';
import { UserService } from '../userService.js';

// Mock the UserStore interface
describe('UserService', () => {
  let userService: UserService;
  let mockStore: {
    getUserById: jest.Mock;
    updateUser: jest.Mock;
  };

  beforeEach(() => {
    mockStore = {
      getUserById: jest.fn(),
      updateUser: jest.fn(),
    };

    const UserStoreMock = jest.fn().mockImplementation(() => mockStore);
    userService = new (UserStoreMock as any)();
  });

  describe('getUserProfile', () => {
    it('returns UserProfileResponse when user exists', () => {
      const userId = '123';
      const expectedProfile: UserProfileResponse = {
        id: userId,
        email: 'test@example.com',
        name: 'Test User',
        created_at: '2023-01-01T00:00:00Z',
      };

      mockStore.getUserById.mockReturnValue({
        ...expectedProfile,
        password_hash: 'hashed',
      } as any);

      const result = userService.getUserProfile(userId);

      expect(result).toEqual(expectedProfile);
      expect(mockStore.getUserById).toHaveBeenCalledWith(userId);
    });

    it('returns ApiError when user not found', () => {
      const userId = 'nonexistent';
      mockStore.getUserById.mockReturnValue(undefined);

      const result = userService.getUserProfile(userId);

      expect(result).toEqual({ error: 'user_not_found' });
      expect(mockStore.getUserById).toHaveBeenCalledWith(userId);
    });
  });

  describe('updateUserProfile', () => {
    const validUserId = '123';
    const validUserData = {
      id: validUserId,
      email: 'test@example.com',
      name: 'Original Name',
      password_hash: 'hashed',
      created_at: '2023-01-01T00:00:00Z',
    };

    beforeEach(() => {
      mockStore.getUserById.mockReturnValue(validUserData as any);
      mockStore.updateUser.mockReturnValue({
        ...validUserData,
        name: 'Updated Name',
      } as any);
    });

    it('updates name and returns UserProfileResponse with HTTP 200 behavior', () => {
      const updateData = { name: 'Updated Name' };

      const result = userService.updateUserProfile(validUserId, updateData);

      expect(result).toEqual({
        id: validUserId,
        email: 'test@example.com',
        name: 'Updated Name',
        created_at: '2023-01-01T00:00:00Z',
      });
      expect(mockStore.updateUser).toHaveBeenCalledWith(validUserId, updateData);
    });

    it('returns name_required error when name is missing', () => {
      const result = userService.updateUserProfile(validUserId, {} as any);

      expect(result).toEqual({ error: 'name_required' });
      expect(mockStore.updateUser).not.toHaveBeenCalled();
    });

    it('returns name_required error when name is empty string', () => {
      const result = userService.updateUserProfile(validUserId, { name: '' });

      expect(result).toEqual({ error: 'name_required' });
      expect(mockStore.updateUser).not.toHaveBeenCalled();
    });

    it('returns name_too_long error when name exceeds 100 characters', () => {
      const longName = 'a'.repeat(101);
      const result = userService.updateUserProfile(validUserId, { name: longName });

      expect(result).toEqual({ error: 'name_too_long' });
      expect(mockStore.updateUser).not.toHaveBeenCalled();
    });

    it('accepts valid name exactly 100 characters', () => {
      const validLongName = 'a'.repeat(100);
      mockStore.updateUser.mockReturnValue({
        ...validUserData,
        name: validLongName,
      } as any);

      const result = userService.updateUserProfile(validUserId, { name: validLongName });

      expect(result).toEqual({
        id: validUserId,
        email: 'test@example.com',
        name: validLongName,
        created_at: '2023-01-01T00:00:00Z',
      });
    });
  });
});