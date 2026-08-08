/**
 * Render the editor status bar: word and page counts, zoom controls and save state.
 *
 * Unresolved imports and exports: none. `react` at L4 is the only import, no `@/` specifier
 * appears, and `Footer` is the default export at L44. It is the one module here that typechecks.
 */
import React from 'react';

/**
 * Show five status readings across three groups.
 *
 * @returns The `footer` element wrapping those three groups.
 * @remarks The component holds no state and registers no handler, so no reading ever updates and
 * the two zoom buttons do nothing. Each reading is a literal string: `Words: 0`, `Pages: 1`,
 * `100%`, `Last saved: Just now` and `Collaborators: 1`.
 *
 * Accessibility: the zoom buttons are labelled `-` and `+` alone, so a screen reader announces one
 * punctuation character, and neither carries `disabled` or `aria-disabled`, so both present as
 * working controls while doing nothing.
 * @example
 * <Footer />
 * Cannot mount today: `App.tsx` imports `store` as a named import of a default-only export.
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