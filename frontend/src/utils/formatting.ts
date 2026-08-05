/**
 * Formatting helpers for the Draft.js editor surface.
 *
 * Both exported functions read the current content and selection from an `EditorState`, apply one
 * change, and return a new `EditorState`. `applyInlineStyle` sets an inline style such as bold.
 * `applyBlockStyle` sets a block type such as a heading.
 *
 * Each function takes two arguments. `handleKeyCommand` in
 * `frontend/src/components/TextEditor.tsx:L17` and `:L24` passes both.
 * `frontend/src/components/Toolbar.tsx:L14` and `:L19` pass one argument each, which binds
 * to `editorState` and leaves the second parameter undefined. `Toolbar.tsx:L31-L33` and
 * `:L36-L38` also pass lowercase names such as `'bold'` and `'heading1'`, which do not match
 * Draft.js constant spellings, and `frontend/src/components/README.md` covers that finding.
 *
 * The import below names `draft-js`, absent from the seven runtime dependencies at
 * `frontend/package.json:L6-L14`, so module resolution fails for this file. The same import names
 * `SelectionState`, which nothing below references. Beyond `draft-js`, the module names no
 * undefined symbol.
 *
 * Line locators: every `Lnn` reference below numbers the tree at commit
 * 06be74c7c88aa6bca652d465eaa00ad480a9e5c5, the frozen revision that precedes this documentation
 * pass. A bare `Lnn` points into this file, and a `path:Lnn` points into the named file. Current
 * HEAD numbers each documented file higher.
 *
 * See `frontend/src/utils/README.md` for the module-level register of these findings.
 */

import { EditorState, Modifier, SelectionState } from 'draft-js';

/**
 * Apply a Draft.js inline style to the current selection and return a new editor state.
 *
 * @param editorState - Editor state supplying the content and selection, read through
 * `getCurrentContent()` and `getSelection()`.
 * @param inlineStyle - Inline style name handed to `Modifier.applyInlineStyle`, such as `'BOLD'`.
 * @returns A new `EditorState` from `EditorState.push`, carrying the change type
 * `'apply-inline-style'`.
 * @remarks
 * The function requires both arguments. `handleKeyCommand` in
 * `frontend/src/components/TextEditor.tsx:L17` passes both.
 * `frontend/src/components/Toolbar.tsx:L14` passes one argument to a two-argument function.
 *
 * The example below cannot run today, because the `draft-js` import above resolves to no
 * installed package.
 * @example
 * ```typescript
 * const next = applyInlineStyle(editorState, 'BOLD');
 * setEditorState(next);
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
 * Set the Draft.js block type of the current selection and return a new editor state.
 *
 * @param editorState - Editor state supplying the content and selection, read through
 * `getCurrentContent()` and `getSelection()`.
 * @param blockType - Block type name handed to `Modifier.setBlockType`, such as
 * `'unstyled'` or `'header-one'`.
 * @returns A new `EditorState` from `EditorState.push`, carrying the change type
 * `'change-block-type'`.
 * @remarks
 * The function requires both arguments. `handleKeyCommand` in
 * `frontend/src/components/TextEditor.tsx:L24` passes both.
 * `frontend/src/components/Toolbar.tsx:L19` passes one argument to a two-argument function.
 *
 * The example below cannot run today, because the `draft-js` import above resolves to no
 * installed package.
 * @example
 * ```typescript
 * const next = applyBlockStyle(editorState, 'header-one');
 * setEditorState(next);
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