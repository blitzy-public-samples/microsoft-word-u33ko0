/**
 * Render the Draft.js editing surface for the open document.
 *
 * Four imported names do not exist: `useAppSelector` and `useAppDispatch` in the
 * store folder, and `selectCurrentDocument` and `updateDocument` in the document
 * slice. `ContentState` is imported and never used. See the HUMAN ASSISTANCE
 * NEEDED marker below.
 *
 * The component declares no props, and `pages/Editor.tsx` passes it two, so the
 * page's content and change handler never reach it.
 *
 * @see ./README.md
 */
import React, { useEffect, useRef } from 'react';
import { Editor, EditorState, ContentState } from 'draft-js';
import { useAppSelector, useAppDispatch } from '@/store';
import { selectCurrentDocument, updateDocument } from '@/store/documentSlice';
import { serializeDocument, deserializeDocument } from '@/utils/documentUtils';

// HUMAN ASSISTANCE NEEDED
// The confidence level for this component is below 0.8. Please review and refine the implementation.

/**
 * Render the editor, loading the open document into it and saving each keystroke.
 *
 * The two Draft.js conversions below are exact inverses of each other, and both are
 * wrong. The effect hands an `EditorState` to `createWithContent`, which expects a
 * `ContentState`, and the change handler hands a `ContentState` to
 * `serializeDocument`, which expects an `EditorState`. Correcting one in isolation
 * leaves the other broken.
 *
 * @returns The canvas element wrapping the Draft.js editor.
 */
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

  /**
   * Store the new editor state and dispatch the serialized content.
   *
   * Serializing the whole document on every keystroke is the cost this handler
   * carries; nothing debounces or batches the work.
   *
   * @param newEditorState - The state Draft.js produced for the edit.
   * @returns Nothing. The dispatched action does not exist, and the spread of a
   * possibly null document would drop the payload's other fields.
   */
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