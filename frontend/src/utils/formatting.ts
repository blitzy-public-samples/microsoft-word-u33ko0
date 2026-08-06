/**
 * Apply Draft.js inline and block formatting to an editor state.
 *
 * Both exported functions read the current content and selection from an `EditorState`, apply one
 * change, and return a new `EditorState`. `applyInlineStyle` sets an inline style such as bold, and
 * `applyBlockStyle` sets a block type such as a heading.
 *
 * The `draft-js` import does not resolve, because `frontend/package.json` omits the package. That
 * same import names `SelectionState`, which nothing below references.
 *
 * @see ./README.md for the module-level register of these findings.
 */
import { EditorState, Modifier, SelectionState } from 'draft-js';

/**
 * Apply an inline style to the current selection and return the resulting editor state.
 *
 * @param editorState - Editor state supplying the content and selection, read through
 * `getCurrentContent()` and `getSelection()`.
 * @param inlineStyle - Inline style name handed to `Modifier.applyInlineStyle`, such as `'BOLD'`.
 * @returns A new `EditorState` from `EditorState.push`, carrying the change type
 * `'apply-inline-style'`.
 * @remarks Both arguments are required. `TextEditor.tsx` passes both, and `Toolbar.tsx` passes one,
 * which binds the style name to `editorState` and leaves `inlineStyle` undefined.
 * @example
 * ```typescript
 * // Cannot run: the `draft-js` import above resolves to no installed package.
 * const next = applyInlineStyle(editorState, 'BOLD');
 * ```
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
 * Change the block type of the current selection and return the resulting editor state.
 *
 * @param editorState - Editor state supplying the content and selection, read through
 * `getCurrentContent()` and `getSelection()`.
 * @param blockType - Block type name handed to `Modifier.setBlockType`, such as `'unstyled'` or
 * `'header-one'`.
 * @returns A new `EditorState` from `EditorState.push`, carrying the change type
 * `'change-block-type'`.
 * @remarks Both arguments are required. `TextEditor.tsx` passes both and uses Draft.js block-type
 * spellings, while `Toolbar.tsx` passes one argument and lowercase names such as `'heading1'`.
 * @example
 * ```typescript
 * // Cannot run: the `draft-js` import above resolves to no installed package.
 * const next = applyBlockStyle(editorState, 'header-one');
 * ```
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