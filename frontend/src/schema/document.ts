/**
 * Declare the client-side runtime validation shapes for a document record and a version snapshot.
 *
 * Line numbers cited for this module refer to the code as committed, before these comment blocks.
 * The module exports two schema values, `DocumentSchema` at L3 and `DocumentVersionSchema` at
 * L13, and no inferred TypeScript type. Both sibling modules declare one, `User` at
 * `schema/user.ts:L13` and `Template` at `schema/template.ts:L12`.
 *
 * @remarks
 * Three modules import a type from here that the module never declares.
 * `store/documentSlice.ts:L2` and `services/collaboration.ts:L3` each request `Document`.
 * `services/api.ts:L3` requests `Document`, `DocumentCreate` and `DocumentUpdate`.
 *
 * Those three import sites name five absent type references. A full type check reports five
 * matching `TS2305` errors, the code TypeScript raises for a missing exported member. All five
 * resolve once the module exports an inferred type.
 *
 * The `zod` import at L1 resolves to nothing. `frontend/package.json:L6-L14` declares seven
 * runtime dependencies, `@reduxjs/toolkit`, `react`, `react-dom`, `react-redux`,
 * `react-router-dom`, `tailwindcss` and `typescript`, and omits `zod`. A type check reports
 * `TS2307` against L1, and no code in this module runs until `zod` is installed.
 *
 * @see ./README.md for the contract drift table covering this directory.
 */
import { z } from 'zod';

/**
 * Validate a complete document record exchanged with the API.
 *
 * @remarks
 * The schema declares seven fields: `id` at L4, `title` at L5, `content` at L6, `owner_id` at L7,
 * `created_at` at L8, `updated_at` at L9, and `collaborators` at L10. `collaborators` holds
 * `z.array(z.string())`. The module calls `.optional()` nowhere, so validation requires every one
 * of the seven.
 *
 * `created_at` at L8 and `updated_at` at L9 declare `z.date()`, which accepts only a JavaScript
 * `Date` instance. The server declares both as `datetime` on its `Document` model at
 * `backend/app/schema/document.py:L93-L94` and sends them as ISO 8601 strings over JSON.
 * `z.date()` rejects a string, so both fields fail against an unconverted API response.
 *
 * The schema names the owner `owner_id` at L7, while `DocumentVersionSchema` names its actor
 * `user_id` at L18. One file therefore carries two names for a reference to a person.
 *
 * `collaborators` at L10 has no server counterpart. `backend/app/schema/document.py` declares no
 * `collaborators` field on any of its five models. The specification models the concept as a
 * Firestore subcollection instead, at `documentation/Technical Specifications.md:L325`.
 *
 * `updated_at` at L9 agrees with the `Document` model at `backend/app/schema/document.py:L94` and
 * differs from `last_modified` at `documentation/Technical Specifications.md:L335`.
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
 * The schema declares five fields, all required: `id` at L14, `document_id` at L15, `content` at
 * L16, `created_at` at L17, and `user_id` at L18.
 *
 * `user_id` at L18 matches the server contract, which declares `user_id` on `DocumentVersion` at
 * `backend/app/schema/document.py:L115`. `DocumentSchema` names the comparable reference
 * `owner_id` at L7.
 *
 * `created_at` at L17 declares `z.date()` and carries the same string-against-`Date` mismatch
 * recorded on `DocumentSchema` above.
 *
 * The specification's Versions subcollection declares `version_id`, `timestamp` and `changes` at
 * `documentation/Technical Specifications.md:L338-L341`. That subcollection declares no author
 * field and no content field, so `user_id` at L18 and `content` at L16 have no counterpart in it.
 */
export const DocumentVersionSchema = z.object({
  id: z.string(),
  document_id: z.string(),
  content: z.string(),
  created_at: z.date(),
  user_id: z.string()
});