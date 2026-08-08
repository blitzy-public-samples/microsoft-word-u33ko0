/**
 * Declare the client-side validation shapes for a document record and a version snapshot.
 *
 * The module exports two schema values, `DocumentSchema` and `DocumentVersionSchema`, and no
 * inferred TypeScript type. Both sibling modules export one, `User` in `schema/user.ts` and
 * `Template` in `schema/template.ts`.
 *
 * @remarks
 * Three modules import types from here that the module never declares, which produces five TS2305
 * errors: `Document` at three import sites, plus `DocumentCreate` and `DocumentUpdate` at
 * `services/api.ts`. Clearing all five needs three exported names, and the server draws the same
 * three-way distinction across `DocumentCreate`, `DocumentUpdate` and `Document` in
 * `backend/app/schema/document.py`.
 *
 * Those three import sites name five absent type references across three distinct missing
 * export names. A full type check reports five matching `TS2305` errors, the code TypeScript
 * raises for a missing exported member. The five errors do not share one cause:
 *
 * - `Document` is missing at three import sites and accounts for three of the errors. One
 *   inferred type export resolves those three and no others.
 * - `DocumentCreate` is missing at one import site and accounts for one error.
 * - `DocumentUpdate` is missing at one import site and accounts for one error.
 *
 * Clearing all five therefore takes three separate exported names, not one. The module
 * currently exports no type at all.
 *
 * The server draws the same three-way distinction. `backend/app/schema/document.py` declares
 * `DocumentCreate` at L68 and `DocumentUpdate` at L82 alongside `Document` at L96, and each
 * carries a different field set. This module declares one schema value covering the full
 * record and none for either write shape, so two of the three contracts have no schema to
 * infer from.
 *
 * All five errors therefore stand as committed, and each importing module fails on the name it
 * asked for rather than on anything in its own file.
 *
 * The `zod` import at L43 resolves to nothing. `frontend/package.json:L6-L14` declares seven
 * runtime dependencies, `@reduxjs/toolkit`, `react`, `react-dom`, `react-redux`,
 * `react-router-dom`, `tailwindcss` and `typescript`, and omits `zod`. A type check reports
 * `TS2307` against L43, and no code in this module runs until `zod` is installed.
 *
 * @see ./README.md for the contract drift table covering this directory.
 */
import { z } from 'zod';

/**
 * Validate a complete document record exchanged with the API.
 *
 * @remarks
 * The schema declares seven required fields: `id`, `title`, `content`, `owner_id`, `created_at`,
 * `updated_at` and `collaborators`, the last holding `z.array(z.string())`. Neither `.optional()`
 * nor `.nullable()` appears, so validation requires all seven and rejects null in all seven.
 *
 * `owner_id` contradicts the server contract on both counts. The Pydantic model declares
 * `owner_id: Optional[str] = None`, so the server may omit the key and may send null, and
 * `z.string()` accepts neither. A response the server considers valid therefore fails this schema.
 *
 * `created_at` and `updated_at` declare `z.date()`, which accepts only a `Date` instance, while the
 * server sends both as ISO 8601 strings over JSON, so both fields fail against an unconverted
 * response.
 *
 * The schema names the owner `owner_id` while `DocumentVersionSchema` names its actor `user_id`, so
 * one file carries two names for a reference to a person. `collaborators` has no counterpart on any
 * model in `backend/app/schema/document.py`.
 */
export const DocumentSchema = z.object({
  id: z.string(),
  title: z.string(),
  content: z.string(),
  owner_id: z.string(),
  created_at: z.date(),
  updated_at: z.date(),
  collaborators: z.array(z.string())
});

/**
 * Validate a historical content snapshot of a document.
 *
 * @remarks
 * The schema declares five required fields: `id`, `document_id`, `content`, `created_at` and
 * `user_id`.
 *
 * `user_id` matches the server, which declares `user_id` on `DocumentVersion`, while
 * `DocumentSchema` names the comparable reference `owner_id`. `created_at` declares `z.date()` and
 * carries the same string-against-`Date` mismatch recorded above.
 */
export const DocumentVersionSchema = z.object({
  id: z.string(),
  document_id: z.string(),
  content: z.string(),
  created_at: z.date(),
  user_id: z.string()
});