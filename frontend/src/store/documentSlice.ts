/**
 * Hold the document slice: the open document, the recent list, loading and error.
 *
 * `Document` is imported from `../schema/document`, which exports two Zod schemas
 * and no inferred type, so the import raises TS2305 and every annotation below
 * that uses it is unresolved.
 *
 * Two components import names this module does not declare: `updateDocument` as an
 * action and `selectCurrentDocument` as a selector. See the HUMAN ASSISTANCE
 * NEEDED marker at the end of the file.
 *
 * @see ./README.md
 */
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Document } from '../schema/document';

/** The slice state: the open document, the recent list, and request status. */
interface DocumentState {
  currentDocument: Document | null;
  recentDocuments: Document[];
  isLoading: boolean;
  error: string | null;
}

/** Opening state: no document, an empty recent list, idle and no error. */
const initialState: DocumentState = {
  currentDocument: null,
  recentDocuments: [],
  isLoading: false,
  error: null,
};

/**
 * Build the `document` slice with six reducers and no async thunk.
 *
 * @remarks Redux Toolkit wraps each reducer with Immer, so the assignments below
 * mutate a draft rather than the live state.
 */
const documentSlice = createSlice({
  name: 'document',
  initialState,
  reducers: {
    /** Replace the open document with the one in the payload. */
    setCurrentDocument: (state, action: PayloadAction<Document>) => {
      state.currentDocument = action.payload;
    },
    /**
     * Push a document onto the front of the recent list, keeping five entries.
     *
     * The slice of the previous list takes four items, so the new head plus four
     * tail entries caps the list at five. The reducer does not deduplicate, so
     * adding the same document twice leaves it in the list twice.
     */
    addRecentDocument: (state, action: PayloadAction<Document>) => {
      state.recentDocuments = [action.payload, ...state.recentDocuments.slice(0, 4)];
    },
    /** Set the in-flight flag for a document request. */
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    /** Set or clear the last document error message. */
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    /** Close the open document, leaving the recent list alone. */
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
    /** Empty the recent list, leaving the open document alone. */
    clearRecentDocuments: (state) => {
      state.recentDocuments = [];
    },
  },
});

/**
 * The six action creators this slice generates, one per reducer above.
 *
 * @example
 * dispatch(setCurrentDocument(doc));
 * dispatch(addRecentDocument(doc));
 * dispatch(clearCurrentDocument());
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