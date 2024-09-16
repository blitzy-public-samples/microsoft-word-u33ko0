import { EditorState, convertToRaw, convertFromRaw } from 'draft-js';
import { DocumentSchema } from '../schema/document';

// HUMAN ASSISTANCE NEEDED
// The following functions may need additional error handling and edge case management for production readiness.
// Also, the DocumentSchema validation needs to be implemented correctly.

export function serializeDocument(editorState: EditorState): string {
  const rawContent = convertToRaw(editorState.getCurrentContent());
  const serializedContent = JSON.stringify(rawContent);
  
  // TODO: Implement proper DocumentSchema validation
  if (!DocumentSchema.isValid(serializedContent)) {
    throw new Error('Serialized content does not match DocumentSchema');
  }
  
  return serializedContent;
}

export function deserializeDocument(serializedContent: string): EditorState {
  let parsedContent;
  
  try {
    parsedContent = JSON.parse(serializedContent);
  } catch (error) {
    throw new Error('Invalid JSON format for serialized content');
  }
  
  // TODO: Implement proper DocumentSchema validation
  if (!DocumentSchema.isValid(parsedContent)) {
    throw new Error('Parsed content does not match DocumentSchema');
  }
  
  const contentState = convertFromRaw(parsedContent);
  return EditorState.createWithContent(contentState);
}