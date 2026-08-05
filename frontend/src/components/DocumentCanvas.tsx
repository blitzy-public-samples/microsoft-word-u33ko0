/** Render the Draft.js editing surface for the open document.
 *
 * useAppSelector, useAppDispatch, selectCurrentDocument, and updateDocument are
 * unresolved.
 * The Editor page requests a named DocumentCanvas export and passes two props, while this
 * component exports a default propless React.FC.
 *
 * The assistance marker immediately above the component records that the implementation
 * needs review.
 */
import React, { useEffect, useRef } from 'react';
import { Editor, EditorState, ContentState } from 'draft-js';
import { useAppSelector, useAppDispatch } from '@/store';
import { selectCurrentDocument, updateDocument } from '@/store/documentSlice';
import { serializeDocument, deserializeDocument } from '@/utils/documentUtils';

// HUMAN ASSISTANCE NEEDED
// The confidence level for this component is below 0.8. Please review and refine the implementation.

/**
 * Render the document editing canvas.
 *
 * @returns The canvas element wrapping the Draft.js editor.
 * @remarks The load helper parses content, then its nonexistent isValid call raises
 * TypeError before editor state replacement. The change path updates local state, then
 * serializeDocument calls getCurrentContent on ContentState and raises before dispatch.
 * Every keystroke reaches that failure. Passing EditorState to createWithContent remains
 * the inverse latent type mismatch. The load path also assumes Draft.js JSON, while the
 * backend Document contract declares content as a free-form string. See the shape notes
 * in utils/documentUtils.
 *
 * @example
 * <DocumentCanvas />
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
   * Store the new editor state and publish the serialized content.
   *
   * @param newEditorState - The state Draft.js reports after an edit.
   * @remarks Local state changes first. Serialization then receives ContentState where it
   * expects EditorState, so getCurrentContent raises before JSON creation or store dispatch.
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