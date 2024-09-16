import { z } from 'zod';

export const TemplateSchema = z.object({
  id: z.string(),
  name: z.string(),
  content: z.string(),
  owner_id: z.string(),
  created_at: z.date(),
  updated_at: z.date()
});

export type Template = z.infer<typeof TemplateSchema>;