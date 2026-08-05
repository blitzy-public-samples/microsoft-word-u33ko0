/**
 * Status bar for the editor shell: word count, page count, zoom level, last-saved time and
 * collaborator count.
 *
 * The module imports only React, so every import resolves and the file typechecks cleanly.
 *
 * All five displayed values are hard-coded literals rather than derived state (L34, L35, L39, L43
 * and L44). The zoom buttons at L38 and L40 declare no `onClick`, so pressing either does nothing.
 *
 * Every `className` is a bespoke semantic name. The repository commits no stylesheet, no
 * `tailwind.config.js` and no `postcss.config.js`, so nothing renders as styled.
 *
 * Line locators: every `Lnn` reference below numbers the tree at commit
 * 06be74c7c88aa6bca652d465eaa00ad480a9e5c5, the frozen revision that precedes this documentation
 * pass. A bare `Lnn` points into this file, and a `path:Lnn` points into the named file. Current
 * HEAD numbers each documented file higher.
 *
 * @see ./README.md for the component inventory of this directory.
 */
import React from 'react';

/**
 * Render the status bar as three groups: document status, zoom controls and additional info.
 *
 * @returns The `footer` element wrapping those three groups.
 * @remarks The component holds no state and registers no handler, so no reading ever updates and
 * the buttons at L38 and L40 do nothing. Each reading is a literal string: `Words: 0` at L34,
 * `Pages: 1` at L35, `100%` at L39, `Last saved: Just now` at L43 and `Collaborators: 1` at L44.
 * @example
 * <Footer />
 * `frontend/src/App.tsx` renders `Footer` in the shell. That shell cannot mount today, because
 * `App.tsx` imports `store` as a named import of a default-only export, and `@/` resolves to
 * nothing.
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