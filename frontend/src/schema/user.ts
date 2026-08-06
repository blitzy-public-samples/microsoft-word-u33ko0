/**
 * Declare the client-side user contract and the static type derived from it.
 *
 * @remarks
 * The `zod` import does not resolve, because `frontend/package.json` omits `zod`, so nothing here
 * runs until the package is installed, and `tsc` reports the unresolved import.
 *
 * The module exports its inferred type, and the sibling `./document.ts` exports none.
 *
 * `UserSchema` declares no `name` field and no `avatar` field, and four call sites read those names
 * across `components/Header.tsx`, `pages/Home.tsx` and `pages/Settings.tsx`.
 *
 * @see ./README.md for the directory-level comparison of the three schema modules.
 */
import { z } from 'zod';

/**
 * Validate a user record the server returns.
 *
 * @remarks
 * The shape declares seven fields: `id`, `email`, `username`, `full_name`, `created_at`,
 * `is_active` and `is_superuser`. `full_name` carries `.optional()` and is the only optional field
 * in this directory, and `email` carries `.email()`, the one format check here.
 *
 * `created_at` declares `z.date()`, which rejects a string, while the server declares
 * `created_at: datetime` and JSON carries that value as an ISO 8601 string, so the declared type
 * contradicts the value the field receives at runtime.
 *
 * The two contracts agree on requiredness for `full_name` and disagree on null. Pydantic's
 * `Optional[str] = None` emits null for an unset value, and Zod's `.optional()` rejects null
 * without `.nullable()` beside it, so a response carrying `full_name: null` fails this schema.
 *
 * The Pydantic `User` model declares `updated_at`, which this schema omits, and `UserCreate`
 * declares `password`, which no schema in this directory models. `is_active` and `is_superuser`
 * match the server, and no committed code path reads either flag.
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
 * Describe a stored user as a static TypeScript type.
 *
 * @remarks
 * `z.infer` reads the compile-time shape from `UserSchema`, so the runtime contract and the static
 * type cannot drift apart inside this module. The alias and `Template` in `./template.ts` are the
 * two inferred types this directory exports, and `./document.ts` exports none. Both importers,
 * `services/auth.ts` and `store/userSlice.ts`, resolve the name.
 */
export type User = z.infer<typeof UserSchema>;