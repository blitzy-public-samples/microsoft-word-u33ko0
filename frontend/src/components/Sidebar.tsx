import React from 'react';
import { StylePanel } from '@/components/StylePanel';
import { CommentPanel } from '@/components/CommentPanel';
import { RevisionPanel } from '@/components/RevisionPanel';

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