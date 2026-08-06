/**
 * Hold the open document, the recent-document list, and the loading and error flags.
 *
 * The module publishes six action creators and its reducer as a default export, and keeps
 * `DocumentState` and `initialState` module-private. Every reducer mutates an Immer draft and
 * returns nothing, which Redux Toolkit commits as the next state.
 *
 * @remarks
 * `@reduxjs/toolkit` is declared in `frontend/package.json`, so `createSlice` resolves. The one
 * unresolved name is local: the `Document` import names a type `schema/document.ts` never
 * declares, which raises TS2305.
 *
 * Four modules import from here and three name symbols this slice never exports.
 * `components/DocumentCanvas.tsx` names `selectCurrentDocument` and `updateDocument`,
 * `components/Toolbar.tsx` names `updateDocument`, and `store/index.ts` names `documentReducer`
 * rather than the default export, which raises TS2614. The assistance marker below asks for
 * asynchronous thunks and error handling, and the slice declares neither.
 *
 * @see ./README.md for the store-level register of these findings.
 */
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Document } from '../schema/document';

/** Shape of the document slice state. */
interface DocumentState {
  currentDocument: Document | null;
  recentDocuments: Document[];
  isLoading: boolean;
  error: string | null;
}

/** Starting state: no open document, an empty recent list, idle and error-free. */
const initialState: DocumentState = {
  currentDocument: null,
  recentDocuments: [],
  isLoading: false,
  error: null,
};

/**
 * Define the `document` slice and its six reducers.
 *
 * @remarks Each reducer mutates the draft state through Immer, which Redux Toolkit applies, so
 * the assignments below produce a new state object rather than mutating the store.
 *
 * - `setCurrentDocument` takes a `Document` and replaces `currentDocument`.
 * - `addRecentDocument` takes a `Document` and prepends it, keeping the first four existing
 *   entries, so `recentDocuments` never holds more than five.
 * - `setLoading` takes a boolean and replaces `isLoading`.
 * - `setError` takes a string or null and replaces `error`.
 * - `clearCurrentDocument` sets `currentDocument` to null and leaves the recent list alone.
 * - `clearRecentDocuments` empties `recentDocuments` and leaves the open document alone.
 *
 * No reducer clears `error` when a later action succeeds, so a stale message survives until a
 * caller dispatches `setError(null)`.
 */
const documentSlice = createSlice({
  name: 'document',
  initialState,
  reducers: {
    /**
     * Store the supplied document as the active document.
     *
     * @param state - Draft slice state.
     * @param action - Action whose `payload` carries the document to store, declared
     * `PayloadAction<Document>`.
     * @returns Nothing.
     * @remarks `pages/Editor.tsx` holds the only dispatch in the codebase, and it runs inside an
     * effect that already requires `currentDocument.id`, so no path seeds the first document.
     * @example
     * ```typescript
     * dispatch(setCurrentDocument(documentData));
     * ```
     */
    setCurrentDocument: (state, action: PayloadAction<Document>) => {
      state.currentDocument = action.payload;
    },
    /**
     * Prepend the supplied document to the recent-document list.
     *
     * @param state - Draft slice state.
     * @param action - Action whose `payload` carries the document to prepend, declared
     * `PayloadAction<Document>`.
     * @returns Nothing.
     * @remarks The list holds at most five entries: the payload goes in front of the first four
     * existing entries, so a full list drops its oldest entry. Duplicate payloads survive, because
     * no entries are compared before prepending.
     */
    addRecentDocument: (state, action: PayloadAction<Document>) => {
      state.recentDocuments = [action.payload, ...state.recentDocuments.slice(0, 4)];
    },
    /**
     * Set the loading flag from the boolean payload.
     *
     * @param state - Draft slice state.
     * @param action - Action whose `payload` is the new flag value, declared
     * `PayloadAction<boolean>`.
     * @returns Nothing. No other reducer in this slice writes that field.
     */
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    /**
     * Record an error message, or clear the stored one.
     *
     * @param state - Draft slice state.
     * @param action - Action whose `payload` is the message to store, declared
     * `PayloadAction<string | null>`, so passing `null` clears the error.
     * @returns Nothing. The reducer leaves `state.isLoading` untouched, unlike the `setError` in
     * `userSlice.ts`, which resets that flag and rejects a `null` payload.
     */
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    /**
     * Drop the active document.
     *
     * @param state - Draft slice state.
     * @returns Nothing. The reducer declares no `action` parameter, so the generated creator takes
     * no argument, and `state.recentDocuments` is left untouched.
     */
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
    /**
     * Empty the recent-document list.
     *
     * @param state - Draft slice state.
     * @returns Nothing. The reducer declares no `action` parameter, so the generated creator takes
     * no argument, and `state.currentDocument` is left untouched.
     */
    clearRecentDocuments: (state) => {
      state.recentDocuments = [];
    },
  },
});

/**
 * Export the six action creators generated from the reducers above.
 *
 * @remarks The first two creators take a document payload, `setLoading` takes a boolean, `setError`
 * takes a string or `null`, and the two clearing creators take no argument. Of the six, only
 * `setCurrentDocument` reaches a consumer.
 *
 * No dispatch can execute today, because `store/index.ts` imports reducer names neither slice
 * declares, so the store never constructs.
 * @example
 * ```typescript
 * dispatch(setLoading(true));
 * dispatch(setError('Save failed'));
 * dispatch(clearCurrentDocument());
 * ```
 */
export const {
  setCurrentDocument,
  addRecentDocument,
  setLoading,
  setError,
  clearCurrentDocument,
  clearRecentDocuments,
} = documentSlice.actions;

/**
 * The slice reducer, exported as the module default for the store's `document` key.
 *
 * @remarks `store/index.ts` imports the name `documentReducer` instead of this default, which is
 * one of the repository's two TS2614 errors.
 */
export default documentSlice.reducer;

// HUMAN ASSISTANCE NEEDED
// Consider adding additional actions or thunks for asynchronous operations
// such as fetching documents from an API or saving documents.
// Also, consider implementing error handling for these operations.