/**
 * Apply Draft.js inline and block formatting to an editor state.
 *
 * Both helpers take the editor state as their first argument and the style as their
 * second. `components/TextEditor.tsx` calls them that way; `components/Toolbar.tsx`
 * passes the style alone and uses lowercase names where Draft.js expects `BOLD` and
 * `unstyled`.
 *
 * `SelectionState` is imported and never used. `draft-js` is imported and
 * `frontend/package.json` does not declare it.
 *
 * @see ./README.md
 */
import { EditorState, Modifier, SelectionState } from 'draft-js';

/**
 * Apply one inline style to the current selection.
 *
 * @param editorState - The editor state to change.
 * @param inlineStyle - A Draft.js inline style name, such as `BOLD` or `ITALIC`.
 * @returns A new editor state carrying the change, pushed as `apply-inline-style`
 * so that a single undo reverses it.
 */
export function applyInlineStyle(editorState: EditorState, inlineStyle: string): EditorState {
  const currentContent = editorState.getCurrentContent();
  const currentSelection = editorState.getSelection();

  const newContent = Modifier.applyInlineStyle(
    currentContent,
    currentSelection,
    inlineStyle
  );

  return EditorState.push(editorState, newContent, 'apply-inline-style');
}

/**
 * Set the block type of every block the selection touches.
 *
 * @param editorState - The editor state to change.
 * @param blockType - A Draft.js block type, such as `unstyled` or `header-one`.
 * @returns A new editor state carrying the change, pushed as `change-block-type`
 * so that a single undo reverses it.
 */
export function applyBlockStyle(editorState: EditorState, blockType: string): EditorState {
  const currentContent = editorState.getCurrentContent();
  const currentSelection = editorState.getSelection();

  const newContent = Modifier.setBlockType(
    currentContent,
    currentSelection,
    blockType
  );

  return EditorState.push(editorState, newContent, 'change-block-type');
}