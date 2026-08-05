/** Compose the editor sidebar from style, comment, and revision panels.
 *
 * The three imported panel modules are unresolved.
 * The Editor page requests a named Sidebar export, but this module exports only a default.
 */
import React from 'react';
import { StylePanel } from '@/components/StylePanel';
import { CommentPanel } from '@/components/CommentPanel';
import { RevisionPanel } from '@/components/RevisionPanel';

/**
 * Render the sidebar panel container.
 *
 * @returns The sidebar element.
 */
const Sidebar: React.FC = () => {
  return (
    <div className="sidebar">
      <StylePanel />
      <CommentPanel />
      <RevisionPanel />
    </div>
  );
};

export default Sidebar;