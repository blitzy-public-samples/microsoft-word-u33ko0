/**
 * Declare the client-side user contract and the static type derived from it.
 *
 * @remarks
 * The `zod` import below does not resolve. `frontend/package.json:L6-L14` declares seven runtime
 * dependencies, `@reduxjs/toolkit`, `react`, `react-dom`, `react-redux`, `react-router-dom`,
 * `tailwindcss` and `typescript`, and omits `zod`. Nothing in this module runs until `zod` is
 * installed, and `tsc` reports the unresolved import against the line below.
 *
 * The module exports its inferred type, and the sibling `./document.ts` exports none.
 *
 * `UserSchema` declares no `name` field and no `avatar` field. Four call sites read those names:
 * `components/Header.tsx:L28` reads `currentUser.avatar` and `currentUser.name`,
 * `components/Header.tsx:L29` reads `currentUser.name`, `pages/Home.tsx:L16` reads
 * `currentUser.name`, and `pages/Settings.tsx:L15` reads `currentUser?.name`.
 *
 * @see ./README.md for the directory-level comparison of the three schema modules.
 */
import { z } from 'zod';

/**
 * Validate a user record the server returns.
 *
 * @remarks
 * The shape declares seven fields: `id`, `email`, `username`, `full_name`, `created_at`,
 * `is_active` and `is_superuser`. `full_name` carries `.optional()` and is the only optional
 * field in this directory. `email` carries `.email()`, so the schema checks address format
 * rather than string type alone, and no other field here constrains a format.
 *
 * `created_at` declares `z.date()`, which accepts a JavaScript `Date` instance and rejects a
 * string. The server declares `created_at: datetime` at `backend/app/schema/user.py:L108`, and
 * JSON carries that value as an ISO 8601 string, so the declared type contradicts the value the
 * field receives at runtime.
 *
 * The Pydantic `User` model at `backend/app/schema/user.py:L107-L111` declares `updated_at` at
 * `user.py:L109`, and `UserSchema` omits the field. `UserCreate` declares `password` at
 * `user.py:L56`, and no schema in this directory models a password. `full_name` stays optional on
 * both sides, matching `user.py:L39`.
 *
 * `is_active` and `is_superuser` are required booleans here and match `user.py:L110-L111`. No
 * code path in the committed tree reads either flag.
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
 * `z.infer` reads the compile-time shape from `UserSchema`, so the runtime contract and the
 * static type cannot drift apart inside this module. The alias and `Template` in
 * `./template.ts` are the two inferred types this directory exports, and `./document.ts` exports
 * none. `services/auth.ts:L3` and `store/userSlice.ts:L2` both resolve the import.
 */
export type User = z.infer<typeof UserSchema>;