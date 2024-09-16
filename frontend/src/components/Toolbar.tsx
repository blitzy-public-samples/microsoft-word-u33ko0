import React from 'react';
import { applyInlineStyle, applyBlockStyle } from '@/utils/formatting';
import { useAppDispatch } from '@/store';
import { updateDocument } from '@/store/documentSlice';

// HUMAN ASSISTANCE NEEDED
// The following component may need additional refinement and error handling for production readiness.
// Please review and adjust as necessary.

const Toolbar: React.FC = () => {
  const dispatch = useAppDispatch();

  const handleInlineStyle = (style: string) => {
    const updatedContent = applyInlineStyle(style);
    dispatch(updateDocument({ content: updatedContent }));
  };

  const handleBlockStyle = (style: string) => {
    const updatedContent = applyBlockStyle(style);
    dispatch(updateDocument({ content: updatedContent }));
  };

  const handleInsert = (type: string) => {
    // TODO: Implement insert functionality
    console.log(`Insert ${type} not implemented yet`);
  };

  return (
    <div className="toolbar">
      <div className="formatting-buttons">
        <button onClick={() => handleInlineStyle('bold')}>Bold</button>
        <button onClick={() => handleInlineStyle('italic')}>Italic</button>
        <button onClick={() => handleInlineStyle('underline')}>Underline</button>
      </div>
      <div className="paragraph-style-buttons">
        <button onClick={() => handleBlockStyle('paragraph')}>Paragraph</button>
        <button onClick={() => handleBlockStyle('heading1')}>Heading 1</button>
        <button onClick={() => handleBlockStyle('heading2')}>Heading 2</button>
      </div>
      <div className="insert-buttons">
        <button onClick={() => handleInsert('table')}>Insert Table</button>
        <button onClick={() => handleInsert('image')}>Insert Image</button>
      </div>
    </div>
  );
};

export default Toolbar;