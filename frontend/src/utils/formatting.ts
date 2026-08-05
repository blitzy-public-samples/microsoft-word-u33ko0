/** Format Draft.js selections with inline and block styles.
 *
 * draft-js is imported but undeclared in frontend/package.json.
 */
import { EditorState, Modifier, SelectionState } from 'draft-js';

/**
 * Apply one inline style across the current selection.
 *
 * @param editorState - The editor state whose content and selection are read.
 * @param inlineStyle - A Draft.js inline style name, such as `BOLD`.
 * @returns A new editor state carrying the restyled content.
 *
 * @example
 * const next = applyInlineStyle(editorState, 'BOLD');
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
 * Apply one block type to every block in the current selection.
 *
 * @param editorState - The editor state whose content and selection are read.
 * @param blockType - A Draft.js block type name, such as `unstyled` or `header-one`.
 * @returns A new editor state carrying the retyped blocks.
 *
 * @example
 * const next = applyBlockStyle(editorState, 'header-one');
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