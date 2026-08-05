/**
 * Convert Draft.js editor content to a JSON string, and rebuild an editor state from that string.
 *
 * Line locators: every `Lnn` reference below numbers the tree at commit
 * 06be74c7c88aa6bca652d465eaa00ad480a9e5c5, the frozen revision that precedes this documentation
 * pass. A bare `Lnn` points into this file, and a `path:Lnn` points into the named file. Current
 * HEAD numbers each documented file higher.
 *
 * `serializeDocument` at L8 reads the current content of an editor state and returns JSON text.
 * `deserializeDocument` at L20 parses JSON text and returns a new editor state.
 *
 * The import at L1 names `draft-js`, absent from the seven runtime dependencies at
 * `frontend/package.json:L6-L14`, so module resolution fails for this file. The import at L2 names
 * `../schema/document`, which resolves to the committed file `frontend/src/schema/document.ts`.
 * The L2 specifier is relative, not the `@/` alias that other frontend modules use. A full type
 * check reports one error against this module, the `TS2307` raised against L1.
 *
 * `DocumentSchema.isValid` at L13 and at L30 names no method. `DocumentSchema` is a Zod object
 * schema declared at `frontend/src/schema/document.ts:L3-L11`. A Zod object exposes `parse` and
 * `safeParse`, and `frontend/src/utils/validation.ts:L5` and `:L14` call `safeParse`.
 *
 * Reading `.isValid` yields `undefined`, so both call sites raise a `TypeError`. Neither guarded
 * `Error` at L14 or at L31 is ever thrown. The compiler flags nothing at L13 or L30, because the
 * unresolved `zod` import leaves `DocumentSchema` untyped.
 *
 * A second fault sits at the same two lines. `DocumentSchema` models document metadata over
 * `id`, `title`, `content`, `owner_id`, `created_at`, `updated_at` and `collaborators`.
 * `convertToRaw()` at L9 yields Draft.js raw content shaped `{ blocks, entityMap }`, which
 * satisfies no field of that schema.
 *
 * The assistance marker at L4 records the authors' note on error handling and on the schema check.
 * The outstanding-work comments at L12 and at L29 mark the two check sites.
 *
 * The only caller inverts both signatures. `frontend/src/components/DocumentCanvas.tsx:L18` binds
 * the `EditorState` returned here to a variable named `contentState`. `:L19` passes that value to
 * `EditorState.createWithContent()`, which expects a `ContentState`. `:L25` passes a
 * `ContentState` from `getCurrentContent()` to `serializeDocument`, which declares an
 * `EditorState`. The two errors are exact inverses of one another.
 *
 * @see frontend/src/utils/README.md for the module-level register of these findings.
 */

import { EditorState, convertToRaw, convertFromRaw } from 'draft-js';
import { DocumentSchema } from '../schema/document';

// HUMAN ASSISTANCE NEEDED
// The following functions may need additional error handling and edge case management for production readiness.
// Also, the DocumentSchema validation needs to be implemented correctly.

/**
 * Convert the current content of an editor state to a JSON string.
 *
 * @param editorState - Editor state read at L9, where `getCurrentContent()` supplies the content
 * that `convertToRaw` converts.
 * @returns The `JSON.stringify` result built at L10 and returned at L17.
 * @remarks
 * L13 guards the return, and L14 throws `Error('Serialized content does not match DocumentSchema')`
 * when that guard rejects. L14 never runs. `DocumentSchema.isValid` at L13 names no method on a
 * Zod object schema, so the call raises a `TypeError` first.
 *
 * L13 also checks the wrong kind of value. The argument is the JSON string built at L10, while
 * `DocumentSchema` at `frontend/src/schema/document.ts:L3-L11` models document metadata.
 *
 * The outstanding-work comment at L12 marks the check.
 *
 * The declared parameter type contradicts the call site.
 * `frontend/src/components/DocumentCanvas.tsx:L25` passes a `ContentState` from
 * `getCurrentContent()` where this signature declares an `EditorState`. `deserializeDocument`
 * carries the opposite error at `DocumentCanvas.tsx:L18-L19`, where an `EditorState` reaches a
 * parameter typed `ContentState`. The two errors are exact inverses of one another.
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
 * @param serializedContent - JSON text that L24 hands to `JSON.parse`.
 * @returns An `EditorState` built at L34 and L35, where `convertFromRaw` produces a `ContentState`
 * and `EditorState.createWithContent` wraps it.
 * @remarks
 * L26 throws `Error('Invalid JSON format for serialized content')` when `JSON.parse` at L24 fails.
 *
 * L30 guards the rest, and L31 throws `Error('Parsed content does not match DocumentSchema')` when
 * that guard rejects. L31 never runs. `DocumentSchema.isValid` at L30 names no method on a Zod
 * object schema, so the call raises a `TypeError` first, exactly as L13 does.
 *
 * L30 and L13 pass different kinds of value to the same check. L30 passes the object that L24
 * parsed. L13 passes the JSON string that L10 built.
 *
 * The outstanding-work comment at L29 marks the check.
 *
 * The declared return type contradicts the call site.
 * `frontend/src/components/DocumentCanvas.tsx:L18` binds this `EditorState` return to a variable
 * named `contentState`. `:L19` passes that value to `EditorState.createWithContent()`, which
 * expects a `ContentState`. `serializeDocument` carries the opposite error at
 * `DocumentCanvas.tsx:L25`, where a `ContentState` reaches a parameter typed `EditorState`. The
 * two errors are exact inverses of one another.
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