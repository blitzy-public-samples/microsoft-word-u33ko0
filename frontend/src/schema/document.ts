/** Define runtime schemas for documents and document versions.
 *
 * The module exports no Document, DocumentCreate, or DocumentUpdate types, and zod is
 * undeclared. Document is requested at three import sites. DocumentCreate and
 * DocumentUpdate are each requested once, so all five failures require three distinct
 * exported names.
 */
import { z } from 'zod';

/**
 * Describe a stored document as the client models it.
 *
 * @remarks Declares `owner_id`, while `DocumentVersionSchema` below declares `user_id`.
 * The `created_at` and `updated_at` fields expect `Date` values, and the server sends ISO
 * strings. The `collaborators` array has no server-side counterpart. The backend permits
 * owner_id to be absent or null, while this schema requires a non-null string.
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
 * Describe one historical snapshot of a document.
 *
 * @remarks Declares `user_id`, while `DocumentSchema` above declares `owner_id`. The
 * `created_at` field expects a `Date` value, and the server sends an ISO string.
 */
export const DocumentVersionSchema = z.object({
  id: z.string(),
  document_id: z.string(),
  content: z.string(),
  created_at: z.date(),
  user_id: z.string()
});