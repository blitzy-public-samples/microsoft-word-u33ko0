/**
 * Render a standalone Draft.js editor with keyboard formatting commands.
 *
 * This file is the argument-count reference only: both calls below pass the editor
 * state and the style, where `components/Toolbar.tsx` passes the style alone. Its block
 * names match Draft.js block types, and its lowercase inline commands do not match the
 * default inline styles, which Draft.js names in upper case.
 *
 * No page or component renders this file, so the working path is unreachable from
 * the application. The `@/` prefix on the helper import raises TS2307.
 *
 * @see ./README.md
 */
import React, { useState } from 'react';
import { Editor, EditorState } from 'draft-js';
import { applyInlineStyle, applyBlockStyle } from '@/utils/formatting';

/**
 * Render the editor and hold its state locally.
 *
 * @returns The Draft.js editor element.
 */
const TextEditor: React.FC = () => {
  const [editorState, setEditorState] = useState(EditorState.createEmpty());

  // HUMAN ASSISTANCE NEEDED
  // The following function needs review and potential improvements for production readiness
  /**
   * Route a Draft.js key command to the inline or block helper.
   *
   * The command name doubles as the style argument, which holds for the block cases
   * and not for the inline ones, because Draft.js names its default inline styles in
   * upper case. Any other command returns `not-handled` so that Draft.js applies its
   * own default. See the HUMAN ASSISTANCE NEEDED marker above.
   *
   * @param command - The Draft.js command name, such as `bold` or `header-one`.
   * @param editorState - The editor state the command applies to. The parameter
   * shadows the component's state variable of the same name.
   * @returns `handled` once a helper produced a new state, `not-handled` otherwise.
   */
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