/**
 * Status bar for the editor shell: word count, page count, zoom level, last-saved time and
 * collaborator count.
 *
 * The module imports only React, so every import resolves and the file typechecks cleanly.
 *
 * All five displayed values are hard-coded literals rather than derived state (L7, L8, L12, L16
 * and L17). The zoom buttons at L11 and L13 declare no `onClick`, so pressing either does nothing.
 *
 * Every `className` is a bespoke semantic name. The repository commits no stylesheet, no
 * `tailwind.config.js` and no `postcss.config.js`, so nothing renders as styled.
 *
 * @see ./README.md for the component inventory of this directory.
 */
import React from 'react';

/**
 * Render the status bar as three groups: document status, zoom controls and additional info.
 *
 * @returns The `footer` element wrapping those three groups.
 * @remarks The component holds no state and registers no handler, so no reading ever updates and
 * the buttons at L11 and L13 do nothing. Each reading is a literal string: `Words: 0` at L7,
 * `Pages: 1` at L8, `100%` at L12, `Last saved: Just now` at L16 and `Collaborators: 1` at L17.
 * @example
 * <Footer />
 * `App.tsx:L26` renders `Footer` in the shell. That shell cannot mount today: `App.tsx:L10`
 * imports `store` as a named import of a default-only export, and `@/` resolves to nothing.
 */
const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="document-status">
        <span className="word-count">Words: 0</span>
        <span className="page-count">Pages: 1</span>
      </div>
      <div className="zoom-controls">
        <button className="zoom-out">-</button>
        <span className="zoom-level">100%</span>
        <button className="zoom-in">+</button>
      </div>
      <div className="additional-info">
        <span className="last-saved">Last saved: Just now</span>
        <span className="collaborators">Collaborators: 1</span>
      </div>
    </footer>
  );
};

export default Footer;