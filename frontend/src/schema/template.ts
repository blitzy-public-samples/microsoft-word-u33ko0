/**
 * Declare the client-side template schema and the `Template` type inferred from it.
 *
 * No module imports either export. `pages/Templates.tsx` declares its own
 * `interface Template` instead, with `description` and `thumbnail` in place of the
 * four fields here. No server-side template schema exists, and
 * `backend/app/api/templates.py` imports one.
 *
 * `zod` is imported and `frontend/package.json` does not declare it.
 *
 * @see ./README.md
 */
import { z } from 'zod';

/**
 * Describe a document template as the client models it.
 *
 * @remarks All six fields are required. The two timestamps declare `z.date()`, so
 * they reject the ISO 8601 strings a JSON response carries.
 */
export const TemplateSchema = z.object({
  id: z.string(),
  name: z.string(),
  content: z.string(),
  owner_id: z.string(),
  created_at: z.date(),
  updated_at: z.date()
});

/** The static `Template` type inferred from `TemplateSchema`. */
export type Template = z.infer<typeof TemplateSchema>;