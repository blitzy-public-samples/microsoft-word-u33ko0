/**
 * Convert between a Draft.js editor state and its serialized JSON form.
 *
 * Both functions call `DocumentSchema.isValid`, which fails twice over. Zod object
 * schemas expose `parse` and `safeParse` rather than `isValid`. `DocumentSchema`
 * also describes document metadata rather than Draft.js content, so it would reject
 * valid content even with the right method. See the HUMAN ASSISTANCE NEEDED marker
 * below and the two TODO markers inside the functions.
 *
 * `draft-js` is imported and `frontend/package.json` does not declare it.
 *
 * @see ./README.md
 */
import { EditorState, convertToRaw, convertFromRaw } from 'draft-js';
import { DocumentSchema } from '../schema/document';

// HUMAN ASSISTANCE NEEDED
// The following functions may need additional error handling and edge case management for production readiness.
// Also, the DocumentSchema validation needs to be implemented correctly.

/**
 * Serialize the content of an editor state to a JSON string.
 *
 * @param editorState - The editor state to serialize.
 * @returns The raw content state as JSON.
 * @throws Error when the validation call below rejects the string, and
 * `TypeError` before that, because `isValid` is not a Zod method.
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
 * @param serializedContent - JSON produced by `serializeDocument`.
 * @returns An editor state carrying the parsed content.
 * @throws Error when the string is not JSON, and `TypeError` at the validation
 * call below, because `isValid` is not a Zod method.
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