// generated_from: behaviors/users/profile
// spec_hash: 0b617acb52c2f132b799bc16470845b2594558e0726d102a13875aa879178b29
// generated_at: 2026-03-15T02:28:14.756106+00:00
// agent: implementation-agent
import { describe, it, expect, vi, beforeEach } from 'vitest';

import { createUserProfileHandler } from './userProfileHandler.js';

import type { UserService } from './userService.js';

import type { Request, Response } from 'some-http-framework';

describe('userProfileHandler', () => {
  let mockUserService: any;
  let mockReq: any;
  let mockRes: any;

  beforeEach(() => {
    mockUserService = {
      getUserProfile: vi.fn(),
      updateUserProfile: vi.fn()
    };

    mockReq = {} as Request<any>;
    mockRes = {
      status: vi.fn().mockReturnThis(),
      json: vi.fn(),
      end: vi.fn()
    } as any;
  });

  describe('getUserProfile', () => {
    it('returns 200 with user profile when user exists', async () => {
      const mockProfile = {
        id: '123',
        email: 'test@example.com',
        name: 'Test User',
        created_at: '2023-01-01T00:00:00Z'
      };
      mockUserService.getUserProfile.mockReturnValue(mockProfile);

      mockReq.params = { id: '123' };
      const { getUserProfile } = createUserProfileHandler(mockUserService as UserService);

      await getUserProfile(mockReq, mockRes);

      expect(mockUserService.getUserProfile).toHaveBeenCalledWith('123');
      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith(mockProfile);
    });

    it('returns 404 when user not found', async () => {
      mockUserService.getUserProfile.mockReturnValue({ error: 'user_not_found' });

      mockReq.params = { id: '123' };
      const { getUserProfile } = createUserProfileHandler(mockUserService as UserService);

      await getUserProfile(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(404);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'user_not_found' });
    });
  });

  describe('updateUserProfile', () => {
    it('returns 200 with updated user when successful', async () => {
      const mockProfile = {
        id: '123',
        email: 'test@example.com',
        name: 'New Name',
        created_at: '2023-01-01T00:00:00Z'
      };
      mockUserService.updateUserProfile.mockReturnValue(mockProfile);

      mockReq.params = { id: '123' };
      mockReq.body = { name: 'New Name' };
      const { updateUserProfile } = createUserProfileHandler(mockUserService as UserService);

      await updateUserProfile(mockReq, mockRes);

      expect(mockUserService.updateUserProfile).toHaveBeenCalledWith('123', { name: 'New Name' });
      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith(mockProfile);
    });

    it('returns 422 name_required when name is missing', async () => {
      mockReq.params = { id: '123' };
      mockReq.body = {};
      const { updateUserProfile } = createUserProfileHandler(mockUserService as UserService);

      await updateUserProfile(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(422);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'name_required' });
    });

    it('returns 422 name_required when name is not string', async () => {
      mockReq.params = { id: '123' };
      mockReq.body = { name: 123 };
      const { updateUserProfile } = createUserProfileHandler(mockUserService as UserService);

      await updateUserProfile(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(422);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'name_required' });
    });

    it('returns 404 when user not found', async () => {
      mockUserService.updateUserProfile.mockReturnValue({ error: 'user_not_found' });

      mockReq.params = { id: '123' };
      mockReq.body = { name: 'New Name' };
      const { updateUserProfile } = createUserProfileHandler(mockUserService as UserService);

      await updateUserProfile(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(404);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'user_not_found' });
    });

    it('returns 422 for validation errors', async () => {
      mockUserService.updateUserProfile.mockReturnValue({ error: 'name_too_long' });

      mockReq.params = { id: '123' };
      mockReq.body = { name: 'a'.repeat(101) };
      const { updateUserProfile } = createUserProfileHandler(mockUserService as UserService);

      await updateUserProfile(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(422);
      expect(mockRes.json).toHaveBeenCalledWith({ error: 'name_too_long' });
    });
  });
});