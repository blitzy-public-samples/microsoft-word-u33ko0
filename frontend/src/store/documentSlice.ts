/**
 * Hold document state for the client as a Redux Toolkit slice.
 *
 * Line numbers cited here refer to the code as committed, before these comment blocks. The module
 * publishes six action creators at L43-L50 and its reducer as a default export at L52, and keeps
 * `DocumentState` at L4-L9 and `initialState` at L11-L16 module-private.
 *
 * @remarks
 * The `Document` import at L2 names a type `schema/document.ts` never declares, so a type check
 * reports `TS2305` against L2. Both sibling schema modules declare an inferred type, `Template` at
 * `schema/template.ts:L12` and `User` in `schema/user.ts`. One export line therefore separates a
 * resolving schema import from this failing one.
 *
 * Four modules import from here and three name symbols this module never exports.
 * `components/DocumentCanvas.tsx:L4` names `selectCurrentDocument` and `updateDocument`, and
 * `components/Toolbar.tsx:L4` names `updateDocument`. `store/index.ts:L2` names `documentReducer`
 * instead of the default export at L52, which TypeScript reports as `TS2614`. Only
 * `pages/Editor.tsx:L8` names an action this slice provides, `setCurrentDocument`.
 *
 * @see ./README.md for the store-level register of these findings.
 */
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Document } from '../schema/document';

interface DocumentState {
  currentDocument: Document | null;
  recentDocuments: Document[];
  isLoading: boolean;
  error: string | null;
}

const initialState: DocumentState = {
  currentDocument: null,
  recentDocuments: [],
  isLoading: false,
  error: null,
};

const documentSlice = createSlice({
  name: 'document',
  initialState,
  reducers: {
    /**
     * Store the supplied document as the active document.
     *
     * @param state - Draft slice state, assigned at L23.
     * @param action - Action whose `payload` carries the document to store, declared
     * `PayloadAction<Document>`.
     * @remarks
     * Redux Toolkit wraps `state` in an Immer draft, so the reducer mutates
     * `state.currentDocument` and returns nothing.
     *
     * `pages/Editor.tsx:L23` holds the only dispatch of this action in the codebase, and the
     * example below reproduces that call. No dispatch runs today, for the reason recorded on the
     * action-creator export at L43.
     * @example
     * ```typescript
     * const documentData = await getDocument(currentDocument.id);
     * dispatch(setCurrentDocument(documentData));
     * ```
     */
    setCurrentDocument: (state, action: PayloadAction<Document>) => {
      state.currentDocument = action.payload;
    },
    /**
     * Prepend the supplied document to the recent-document list.
     *
     * @param state - Draft slice state, assigned at L26.
     * @param action - Action whose `payload` carries the document to prepend, declared
     * `PayloadAction<Document>`.
     * @remarks
     * The list holds at most five entries. L26 keeps the first four existing entries and puts the
     * payload in front of them, so a full list drops its oldest entry on the next call.
     *
     * The reducer writes `state.recentDocuments` through the Immer draft and returns nothing.
     * Duplicate payloads survive, because L26 compares no entries before prepending.
     *
     * The example cannot run today, for the reason recorded at L43.
     * @example
     * ```typescript
     * dispatch(addRecentDocument(documentData));
     * ```
     */
    addRecentDocument: (state, action: PayloadAction<Document>) => {
      state.recentDocuments = [action.payload, ...state.recentDocuments.slice(0, 4)];
    },
    /**
     * Set the loading flag from the boolean payload.
     *
     * @param state - Draft slice state, assigned at L29.
     * @param action - Action whose `payload` is the new flag value, declared
     * `PayloadAction<boolean>`.
     * @remarks
     * The reducer writes `state.isLoading` through the Immer draft and returns nothing. No other
     * reducer in this slice writes that field.
     */
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    /**
     * Record an error message, or clear the stored one.
     *
     * @param state - Draft slice state, assigned at L32.
     * @param action - Action whose `payload` is the message to store, declared
     * `PayloadAction<string | null>`, so passing `null` clears the error.
     * @remarks
     * The reducer writes `state.error` through the Immer draft and returns nothing, and leaves
     * `state.isLoading` untouched.
     *
     * `userSlice.ts:L37` declares `PayloadAction<string>` for its own `setError`, which rejects
     * `null`. That slice clears `state.error` through `setUser` at `userSlice.ts:L26` and
     * `clearUser` at `userSlice.ts:L32` instead, and its `setError` also resets `isLoading`.
     */
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    /**
     * Drop the active document.
     *
     * @param state - Draft slice state, assigned at L35.
     * @remarks
     * The reducer declares no `action` parameter at L34, so the generated action creator takes no
     * argument. Assigning `null` at L35 leaves `state.recentDocuments` untouched.
     */
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
    /**
     * Empty the recent-document list.
     *
     * @param state - Draft slice state, assigned at L38.
     * @remarks
     * The reducer declares no `action` parameter at L37, so the generated action creator takes no
     * argument. Assigning a fresh empty array at L38 leaves `state.currentDocument` untouched.
     */
    clearRecentDocuments: (state) => {
      state.recentDocuments = [];
    },
  },
});

/**
 * Publish the six action creators generated for this slice.
 *
 * @remarks
 * The destructure at L43-L50 exports `setCurrentDocument`, `addRecentDocument`, `setLoading`,
 * `setError`, `clearCurrentDocument` and `clearRecentDocuments`. The first two take a document
 * payload, `setLoading` takes a boolean, `setError` takes a string or `null`, and the two clearing
 * creators take no argument.
 *
 * No dispatch below can execute today, because `store/index.ts:L2-L3` imports `documentReducer`
 * and `userReducer`, which neither slice declares. The reducer map at `store/index.ts:L6-L9`
 * therefore binds two undefined values, and the store never constructs.
 *
 * Of the six creators, only `setCurrentDocument` reaches a consumer, at `pages/Editor.tsx:L8`.
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

export default documentSlice.reducer;

// HUMAN ASSISTANCE NEEDED
// Consider adding additional actions or thunks for asynchronous operations
// such as fetching documents from an API or saving documents.
// Also, consider implementing error handling for these operations.