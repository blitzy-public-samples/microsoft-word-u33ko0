/** Render the template gallery: fetch templates once on mount and show them as clickable cards.
 *
 * Every `L` reference below numbers a file as committed, before any comment block was added.
 *
 * All five `@/` specifiers fail module resolution, because `frontend/tsconfig.json:L10-L16`
 * declares `@components/*`, `@utils/*`, `@styles/*`, `@hooks/*` and `@services/*` and no `@/*`.
 * Three also name a missing symbol. `getTemplates` (L4) is absent from `services/api.ts`, which
 * exports only `getDocuments` (L38), `createDocument` (L43) and `updateDocument` (L48) and holds
 * no template endpoint. `useAppSelector` (L5) is absent from `store/index.ts`, which exports only
 * `RootState` (L12), `AppDispatch` (L13) and a default `store` (L15). `selectCurrentUser` (L6) is
 * absent from `store/userSlice.ts:L44`, which exports only `setUser`, `clearUser`, `setLoading`
 * and `setError`. `Header` (L2) and `Footer` (L3) name default-only exports at
 * `components/Header.tsx:L42` and `components/Footer.tsx:L23`; `pages/Home.tsx:L3-L4` writes both
 * as defaults, the form those modules export.
 *
 * `Template` names two different shapes. The local `interface Template` (L8-L13) declares `id`,
 * `name`, `description` and `thumbnail`, while `schema/template.ts:L3-L10` declares `id`, `name`,
 * `content`, `owner_id`, `created_at` and `updated_at` and exports its inferred type at L12. The
 * two share `id` and `name` only, and this file never imports the schema.
 *
 * The assistance markers at L27 and L37 record error handling and post-selection navigation as
 * unfinished.
 *
 * @see ./README.md
 */
import React, { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { getTemplates } from '@/services/api';
import { useAppSelector } from '@/store';
import { selectCurrentUser } from '@/store/userSlice';

interface Template {
  id: string;
  name: string;
  description: string;
  thumbnail: string;
}

/**
 * Render the templates page: a heading above one clickable card per fetched template.
 *
 * @returns The templates page element.
 *
 * @remarks Two values are written and never read. `selectedTemplate` (L17) is assigned at L36, and
 * no branch, effect or handler reads it. `currentUser` (L18) is never rendered and never passed on.
 *
 * The effect at L20-L33 closes with an empty dependency array (L33), so the fetch runs once on
 * mount and the gallery never refreshes. A failed fetch writes to the console at L26 and leaves
 * `templates` empty, so the page then renders the heading above no cards.
 *
 * Side effects: one network call (L23), two state writes (L24 and L36), one store read (L18) and
 * one console write (L26). The component dispatches no action and performs no navigation.
 *
 * `App.tsx:L17` renders `Header` and `App.tsx:L26` renders `Footer` around every route, so L43
 * and L64 here add a second header and a second footer.
 *
 * Both styling conventions appear in this one file. L42 uses the bespoke name `templates-page`,
 * L44, L45, L46, L56, L58 and L59 use Tailwind utilities, and L50 combines the bespoke
 * `template-card` with Tailwind utilities inside a single attribute. Neither convention renders:
 * `frontend/package.json:L12` declares `tailwindcss`, and the repository commits no
 * `tailwind.config.js`, no `postcss.config.js` and no stylesheet.
 *
 * The route below cannot render today. The five unresolved specifiers stop the bundle from
 * compiling, so no heading and no card reach the screen.
 *
 * @example
 *     <Route path="/templates" component={Templates} />
 */
const Templates: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const currentUser = useAppSelector(selectCurrentUser);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const fetchedTemplates = await getTemplates();
        setTemplates(fetchedTemplates);
      } catch (error) {
        console.error('Error fetching templates:', error);
        // HUMAN ASSISTANCE NEEDED
        // TODO: Implement proper error handling and user feedback
      }
    };

    fetchTemplates();
  }, []);

  /**
   * Store the identifier of the template card the reader clicked.
   *
   * @param templateId - Identifier of the clicked template, passed from `template.id` at L51.
   * @returns Nothing. The declared result is `void`.
   *
   * @remarks The handler is terminal. L36 writes `templateId` into `selectedTemplate`, which
   * nothing reads, and the function then ends. Clicking a card therefore changes no visible
   * output and starts no navigation. The outstanding-work comment at L38 records the navigation
   * step as unfinished.
   */
  const handleTemplateSelection = (templateId: string) => {
    setSelectedTemplate(templateId);
    // HUMAN ASSISTANCE NEEDED
    // TODO: Implement navigation to template editing page or next step in the process
  };

  return (
    <div className="templates-page">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Document Templates</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((template) => (
            <div
              key={template.id}
              className="template-card border rounded-lg p-4 cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => handleTemplateSelection(template.id)}
            >
              <img
                src={template.thumbnail}
                alt={template.name}
                className="w-full h-40 object-cover mb-4 rounded"
              />
              <h2 className="text-xl font-semibold mb-2">{template.name}</h2>
              <p className="text-gray-600">{template.description}</p>
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Templates;