/**
 * Render the editor side panel: styles, comments and revisions.
 *
 * All three panel modules are imported and none exists in the tree, so this file
 * raises three TS2307 errors and the component cannot render.
 *
 * @see ./README.md
 */
import React from 'react';
import { StylePanel } from '@/components/StylePanel';
import { CommentPanel } from '@/components/CommentPanel';
import { RevisionPanel } from '@/components/RevisionPanel';

/**
 * Render the three panels, unconditionally and with no props.
 *
 * Nothing toggles a panel and nothing collapses the container, so the intended
 * panel switching described in the specification has no implementation here.
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