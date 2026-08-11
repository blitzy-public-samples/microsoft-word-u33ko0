/**
 * Declare the client-side user schema and the `User` type inferred from it.
 *
 * `store/userSlice.ts` imports `User` from here, and that import resolves.
 * `zod` is imported and `frontend/package.json` does not declare it.
 *
 * @see ./README.md
 */
import { z } from 'zod';

/**
 * Describe a user account as the client models it.
 *
 * @remarks The email field carries a format check, the only validation rule in the
 * schema folder. `updated_at` is absent here and required by the server contract,
 * so a parsed server response drops it. `created_at` declares `z.date()`, which
 * rejects the ISO 8601 string a JSON response carries.
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

/** The static `User` type inferred from `UserSchema`. */
export type User = z.infer<typeof UserSchema>;