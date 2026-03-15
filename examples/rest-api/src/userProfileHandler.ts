// generated_from: behaviors/users/profile
// spec_hash: 0b617acb52c2f132b799bc16470845b2594558e0726d102a13875aa879178b29
// generated_at: 2026-03-15T02:28:14.754691+00:00
// agent: implementation-agent
import type { Request, Response } from 'some-http-framework';

import type { UserService } from './userService.js';

export function createUserProfileHandler(userService: UserService): {
  getUserProfile: (req: Request<{ params: { id: string } }>, res: Response) => Promise<void>;
  updateUserProfile: (req: Request<{ params: { id: string } }, { body: unknown }>, res: Response) => Promise<void>;
} {
  return {
    getUserProfile: async (req, res) => {
      const result = userService.getUserProfile(req.params.id);
      if ('error' in result) {
        res.status(404).json(result);
      } else {
        res.status(200).json(result);
      }
    },

    updateUserProfile: async (req, res) => {
      const body = req.body as Record<string, unknown>;
      const name = body.name as string | undefined;

      if (typeof name !== 'string') {
        res.status(422).json({ error: 'name_required' });
        return;
      }

      const result = userService.updateUserProfile(req.params.id, { name });
      if ('error' in result) {
        if (result.error === 'user_not_found') {
          res.status(404).json(result);
        } else {
          res.status(422).json(result);
        }
      } else {
        res.status(200).json(result);
      }
    }
  };
}