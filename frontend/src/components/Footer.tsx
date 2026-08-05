/** Render the editor's static status bar; all displayed values are literals.
 *
 * App and Home import the default export correctly. Settings and Templates request a named
 * Footer export that this module does not provide.
 */
import React from 'react';

/**
 * Render document status, zoom controls, and collaborator information.
 *
 * The five status values are hard-coded. Both zoom buttons have no handler.
 *
 * @returns The footer element.
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