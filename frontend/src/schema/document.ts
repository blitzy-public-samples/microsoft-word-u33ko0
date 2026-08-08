/**
 * Declare the client-side document and version schemas.
 *
 * This module exports no inferred type, unlike its two siblings, which each export
 * one. That single omission is the root cause of six TS2305 and TS2614 failures:
 * `store/documentSlice.ts`, `services/api.ts` and `services/collaboration.ts` each
 * import a `Document` type from here.
 *
 * `zod` is imported and `frontend/package.json` does not declare it.
 *
 * @see ./README.md
 */
import { z } from 'zod';

/**
 * Describe a document as the client models it.
 *
 * @remarks Every field is required, including `owner_id`, while the server contract
 * makes it optional. `collaborators` has no server counterpart at all. The two
 * timestamps declare `z.date()`, so they reject the ISO 8601 strings a JSON
 * response carries.
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
 * Describe one stored revision of a document.
 *
 * @remarks The actor field is `user_id` here and `owner_id` on the document above,
 * so one file carries two names for ownership. No module imports this schema.
 */
export const DocumentVersionSchema = z.object({
  id: z.string(),
  document_id: z.string(),
  content: z.string(),
  created_at: z.date(),
  user_id: z.string()
});