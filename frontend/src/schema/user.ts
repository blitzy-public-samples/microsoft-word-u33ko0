/** Define the client-side user schema and its inferred TypeScript type.
 *
 * zod is imported but undeclared in frontend/package.json.
 */
import { z } from 'zod';

/**
 * Describe a user record as the client models it.
 *
 * @remarks The `created_at` field expects a `Date` value, and the server sends an ISO
 * string. The schema omits `updated_at`, which the server contract declares. The backend
 * accepts full_name as missing or null. Zod optional accepts missing or undefined but
 * rejects null, so a valid backend value can fail this schema.
 */
export const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  username: z.string(),
  full_name: z.string().optional(),
  created_at: z.date(),
  is_active: z.boolean(),
  is_superuser: z.boolean()
});

/**
 * Represent a validated user record in TypeScript, inferred from `UserSchema`.
 */
export type User = z.infer<typeof UserSchema>;