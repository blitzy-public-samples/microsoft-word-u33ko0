/** Define the client-side template schema and inferred Template type.
 *
 * zod is imported but undeclared. The seven runtime dependencies in
 * frontend/package.json:L6-L14 omit it, so nothing in this module runs until zod is installed.
 *
 * No module imports `TemplateSchema` or `Template`. The template page declares its own
 * `interface Template` in pages/Templates.tsx and never imports this file. The two shapes share
 * `id` and `name`, the page adds `description` and `thumbnail`, and this schema adds `content`,
 * `owner_id`, `created_at` and `updated_at`.
 *
 * The server half of the contract is missing. No backend/app/schema/template.py exists, and
 * backend/app/api/templates.py:L70 imports it. The same router imports the absent template
 * service at L32.
 *
 * Every `Lnn` locator here points at the current layout of the file it names. A bare
 * `Lnn` points into this file, and a `path:Lnn` points into the named file.
 *
 * @see ./README.md
 */
import { z } from 'zod';

/**
 * Describe a document template as the client models it.
 *
 * @remarks All six fields are required: `id`, `name`, `content`, `owner_id`, `created_at`
 * and `updated_at`. The two timestamps declare `z.date()`, so they accept a `Date` instance
 * and reject the ISO 8601 strings a JSON response carries. No server-side template schema
 * exists, so nothing constrains these names or types from the other end.
 */
export const TemplateSchema = z.object({
  id: z.string(),
  name: z.string(),
  content: z.string(),
  owner_id: z.string(),
  created_at: z.date(),
  updated_at: z.date()
});

/** Infer the static Template type from TemplateSchema. */
export type Template = z.infer<typeof TemplateSchema>;