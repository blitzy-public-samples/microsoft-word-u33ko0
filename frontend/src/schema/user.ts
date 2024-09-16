import { z } from 'zod';

export const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  username: z.string(),
  full_name: z.string().optional(),
  created_at: z.date(),
  is_active: z.boolean(),
  is_superuser: z.boolean()
});

export type User = z.infer<typeof UserSchema>;