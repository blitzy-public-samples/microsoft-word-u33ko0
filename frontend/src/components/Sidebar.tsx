/**
 * Compose the editor sidebar from style, comment, and revision panels.
 *
 * None of the three panel modules exists under `components/`, and the `@/` prefix is absent
 * from the `tsconfig` path aliases, so each import fails on both counts.
 */
import React from 'react';
import { StylePanel } from '@/components/StylePanel';
import { CommentPanel } from '@/components/CommentPanel';
import { RevisionPanel } from '@/components/RevisionPanel';

/**
 * Stack the three panels in one container, unconditionally and in fixed order.
 *
 * @returns The sidebar element.
 * @remarks Intended behavior per `documentation/Technical Specifications.md`, "USER INTERFACE
 * DESIGN" heading: the sidebar hosts formatting, comment and revision panels, which matches
 * the three names imported here.
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