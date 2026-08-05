/** Serialize and deserialize Draft.js editor state.
 *
 * draft-js is imported but undeclared in frontend/package.json. The assistance
 * marker below records the unresolved error-handling and schema-validation work.
 */
import { EditorState, convertToRaw, convertFromRaw } from 'draft-js';
import { DocumentSchema } from '../schema/document';

// HUMAN ASSISTANCE NEEDED
// The following functions may need additional error handling and edge case management for production readiness.
// Also, the DocumentSchema validation needs to be implemented correctly.

/**
 * Serialize the editor's current content to a JSON string.
 *
 * @param editorState - The editor state to serialize.
 * @returns The serialized raw content state.
 * @remarks `DocumentSchema.isValid` is not part of the Zod API, so the guard throws a
 * TypeError before its declared Error can be reached.
 */
export function serializeDocument(editorState: EditorState): string {
  const rawContent = convertToRaw(editorState.getCurrentContent());
  const serializedContent = JSON.stringify(rawContent);
  
  // TODO: Implement proper DocumentSchema validation
  if (!DocumentSchema.isValid(serializedContent)) {
    throw new Error('Serialized content does not match DocumentSchema');
  }
  
  return serializedContent;
}

/**
 * Rebuild an editor state from a serialized raw content string.
 *
 * @param serializedContent - The JSON string produced by `serializeDocument`.
 * @returns An editor state holding the parsed content.
 * @remarks `DocumentSchema.isValid` is not part of the Zod API, so the schema guard
 * throws a TypeError before its declared Error can be reached. Invalid JSON is rejected
 * earlier with the declared Error.
 */
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