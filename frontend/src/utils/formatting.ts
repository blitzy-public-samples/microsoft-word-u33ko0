import { EditorState, Modifier, SelectionState } from 'draft-js';

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