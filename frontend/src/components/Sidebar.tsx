/**
 * Composes the editor sidebar from three panel modules, and `pages/Editor.tsx:L60` renders the
 * component beside the document canvas. Line numbers below cite the committed file.
 *
 * The component cannot render. The three panel imports name `@/components/StylePanel` at L2,
 * `@/components/CommentPanel` at L3 and `@/components/RevisionPanel` at L4. No such file exists
 * under `frontend/src/components/`, which holds eight components and none of these three. L9
 * through L11 render all three unconditionally, so one absent panel stops the whole subtree.
 *
 * The `@/` prefix does not resolve either, because `frontend/tsconfig.json:L10-L16` omits `@/*`.
 * L2 through L4 also request named bindings, while all eight components in this directory export
 * a default. See `./README.md` for the directory-level defect register.
 */
import React from 'react';
import { StylePanel } from '@/components/StylePanel';
import { CommentPanel } from '@/components/CommentPanel';
import { RevisionPanel } from '@/components/RevisionPanel';

/**
 * Render a `div.sidebar` wrapping the style, comment and revision panels in that order.
 *
 * @returns A `div` element carrying class `sidebar` and holding the three panel elements.
 * @remarks The render never completes, because L2 through L4 import modules that do not exist.
 * Intended behavior per documentation/Technical Specifications.md, "USER INTERFACE DESIGN" heading:
 * the sidebar composes `StylesPanel`, `CommentsPanel` and `VersionHistoryPanel` at L474-L476, none
 * of them a name this module imports.
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