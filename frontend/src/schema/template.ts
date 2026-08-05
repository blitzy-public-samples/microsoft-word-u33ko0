/** Define the client-side validation shape for a document template and its inferred type.
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
 * backend/app/api/templates.py:L13 imports it. The same router imports the absent template
 * service at L14.
 *
 * @see ./README.md
 */
import { z } from 'zod';

/**
 * Describe a document template as the client models it.
 *
 * @remarks All six fields are required. The schema declares no `.optional()` and no format
 * constraint, so `id`, `name`, `content` and `owner_id` accept any string. The `created_at` and
 * `updated_at` fields expect `Date` values and reject strings, while JSON responses carry
 * timestamps as ISO 8601 strings. The `owner_id` name matches `DocumentSchema.owner_id` at
 * ./document.ts:L7, so the two client schemas agree on the owner field. No
 * backend/app/schema/template.py exists, so no server contract constrains these names or types.
 */
export const TemplateSchema = z.object({
  id: z.string(),
  name: z.string(),
  content: z.string(),
  owner_id: z.string(),
  created_at: z.date(),
  updated_at: z.date()
});

/**
 * Represent a validated document template in TypeScript, inferred from `TemplateSchema`.
 *
 * @remarks `z.infer` derives the alias from the schema above, so the runtime shape and the
 * compile-time type cannot diverge inside this module. Nothing imports the alias, and the
 * template page uses its own local `Template` instead. ./user.ts:L13 also exports an inferred
 * type, while ./document.ts exports none.
 */
export type Template = z.infer<typeof TemplateSchema>;