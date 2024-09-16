import React, { useState } from 'react';
import { Editor, EditorState } from 'draft-js';
import { applyInlineStyle, applyBlockStyle } from '@/utils/formatting';

const TextEditor: React.FC = () => {
  const [editorState, setEditorState] = useState(EditorState.createEmpty());

  // HUMAN ASSISTANCE NEEDED
  // The following function needs review and potential improvements for production readiness
  const handleKeyCommand = (command: string, editorState: EditorState) => {
    let newState: EditorState | null = null;

    switch (command) {
      case 'bold':
      case 'italic':
      case 'underline':
        newState = applyInlineStyle(editorState, command);
        break;
      case 'header-one':
      case 'header-two':
      case 'blockquote':
      case 'unordered-list-item':
      case 'ordered-list-item':
        newState = applyBlockStyle(editorState, command);
        break;
      default:
        return 'not-handled';
    }

    if (newState) {
      setEditorState(newState);
      return 'handled';
    }

    return 'not-handled';
  };

  return (
    <Editor
      editorState={editorState}
      onChange={setEditorState}
      handleKeyCommand={handleKeyCommand}
    />
  );
};

export default TextEditor;