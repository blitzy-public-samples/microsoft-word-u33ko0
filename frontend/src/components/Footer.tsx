/**
 * Render the editor status bar: word and page counts, zoom controls and save state.
 */
import React from 'react';

/**
 * Show six status readings across three groups.
 *
 * @returns The `footer` element wrapping those three groups.
 * @remarks The component holds no state and registers no handler, so no reading ever updates and
 * the two zoom buttons do nothing. Each reading is a literal string: `Words: 0`, `Pages: 1`,
 * `100%`, `Last saved: Just now` and `Collaborators: 1`.
 *
 * Accessibility: the zoom buttons carry the labels `-` and `+` and nothing else, so a screen reader
 * announces a single punctuation character rather than "zoom out" or "zoom in". Neither button
 * carries a `disabled` or `aria-disabled` attribute, so both present themselves as working controls
 * while doing nothing.
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