import React, { useEffect, useRef } from 'react';
import { Editor, EditorState, ContentState } from 'draft-js';
import { useAppSelector, useAppDispatch } from '@/store';
import { selectCurrentDocument, updateDocument } from '@/store/documentSlice';
import { serializeDocument, deserializeDocument } from '@/utils/documentUtils';

// HUMAN ASSISTANCE NEEDED
// The confidence level for this component is below 0.8. Please review and refine the implementation.

const DocumentCanvas: React.FC = () => {
  const dispatch = useAppDispatch();
  const currentDocument = useAppSelector(selectCurrentDocument);
  const [editorState, setEditorState] = React.useState(() => EditorState.createEmpty());
  const editorRef = useRef<Editor>(null);

  useEffect(() => {
    if (currentDocument) {
      const contentState = deserializeDocument(currentDocument.content);
      setEditorState(EditorState.createWithContent(contentState));
    }
  }, [currentDocument]);

  const handleEditorChange = (newEditorState: EditorState) => {
    setEditorState(newEditorState);
    const serializedContent = serializeDocument(newEditorState.getCurrentContent());
    dispatch(updateDocument({ ...currentDocument, content: serializedContent }));
  };

  return (
    <div className="document-canvas">
      <Editor
        ref={editorRef}
        editorState={editorState}
        onChange={handleEditorChange}
      />
    </div>
  );
};

export default DocumentCanvas;