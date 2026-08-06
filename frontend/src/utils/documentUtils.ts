/**
 * Convert Draft.js editor content to and from a serialized JSON string.
 *
 * `serializeDocument` reads the current content of an editor state and returns JSON text, and
 * `deserializeDocument` parses JSON text and returns a new editor state. The `draft-js` import does
 * not resolve, because `frontend/package.json` omits the package, and that is the one type error
 * reported against this module.
 *
 * `DocumentSchema.isValid` names no method, and both call sites carry the same two faults. A Zod
 * object schema exposes `parse` and `safeParse`, so reading `.isValid` yields `undefined` and each
 * call raises a `TypeError` before its guarded `Error` can throw. The schema is also the wrong one,
 * since `DocumentSchema` models document metadata while the checked values are Draft.js raw content
 * and its JSON text. The marker and the two outstanding-work comments below mark both sites.
 *
 * The one caller inverts both signatures. `components/DocumentCanvas.tsx` binds the `EditorState`
 * returned here to a variable named `contentState` and hands it to `EditorState.createWithContent`,
 * which expects a `ContentState`, then passes a `ContentState` to `serializeDocument`.
 *
 * @see ./README.md for the module-level register of these findings.
 */
import { EditorState, convertToRaw, convertFromRaw } from 'draft-js';
import { DocumentSchema } from '../schema/document';

// HUMAN ASSISTANCE NEEDED
// The following functions may need additional error handling and edge case management for production readiness.
// Also, the DocumentSchema validation needs to be implemented correctly.

/**
 * Serialize the editor's current content to a JSON string.
 *
 * @param editorState - Editor state whose `getCurrentContent()` result `convertToRaw` converts.
 * @returns The `JSON.stringify` result.
 * @remarks The guard before the return calls `DocumentSchema.isValid` on the JSON string, so the
 * function raises a `TypeError` there and its `Error('Serialized content does not match
 * DocumentSchema')` never throws. The module header records both faults in that guard.
 *
 * The declared parameter contradicts the one caller, which passes a `ContentState`.
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
 * Rebuild an editor state from a serialized JSON string.
 *
 * @param serializedContent - JSON text handed to `JSON.parse`.
 * @returns An `EditorState` wrapping the `ContentState` that `convertFromRaw` produces.
 * @remarks A parse failure throws `Error('Invalid JSON format for serialized content')`, which is
 * the one error this module can actually raise. The guard that follows calls
 * `DocumentSchema.isValid` on the parsed object, so the function raises a `TypeError` there and its
 * `Error('Parsed content does not match DocumentSchema')` never throws.
 *
 * The declared return contradicts the one caller, which treats the value as a `ContentState`.
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