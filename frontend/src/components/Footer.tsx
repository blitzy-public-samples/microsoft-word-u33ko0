/**
 * Render the status bar beneath the editor.
 *
 * Every value shown is a literal in the markup: the word count, page count, zoom
 * level, last-saved time and collaborator count. The component reads no store state
 * and takes no props, so none of the five changes at runtime.
 *
 * @see ./README.md
 */
import React from 'react';

/**
 * Render the document status, the zoom controls and the collaboration summary.
 *
 * The two zoom buttons carry no `onClick` handler, so pressing either does nothing.
 * The class names are bespoke rather than Tailwind utilities, and the repository
 * commits no stylesheet, so none of them resolves to a rule.
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