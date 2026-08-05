/** Manage the active document, recent documents, loading state, and errors.
 *
 * @reduxjs/toolkit is declared in frontend/package.json, so that import resolves.
 * Document and documentReducer imports expected by consumers are unresolved.
 * The assistance marker at the end records missing asynchronous fetch/save actions and
 * error handling. No thunk or extraReducers block implements either concern.
 */
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Document } from '../schema/document';

/** The open document, the recent-document list, and the status flags. */
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
     * Replace the open document.
     *
     * @param state - The document slice state.
     * @param action - Action whose payload is the document to make current.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    setCurrentDocument: (state, action: PayloadAction<Document>) => {
      state.currentDocument = action.payload;
    },
    /**
     * Prepend a document to the recent list and cap the list at five entries.
     *
     * @param state - The document slice state.
     * @param action - Action whose payload is the document to record.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    addRecentDocument: (state, action: PayloadAction<Document>) => {
      state.recentDocuments = [action.payload, ...state.recentDocuments.slice(0, 4)];
    },
    /**
     * Set the loading flag.
     *
     * @param state - The document slice state.
     * @param action - Action whose payload is the new flag value.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    /**
     * Record an error message, or clear it with a null payload.
     *
     * @param state - The document slice state.
     * @param action - Action whose payload is the message or null.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    /**
     * Clear the open document.
     *
     * @param state - The document slice state.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
    /**
     * Empty the recent-document list.
     *
     * @param state - The document slice state.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    clearRecentDocuments: (state) => {
      state.recentDocuments = [];
    },
  },
});

/**
 * The slice's action creators.
 *
 * @example
 * dispatch(setCurrentDocument(document));
 */
export const {
  setCurrentDocument,
  addRecentDocument,
  setLoading,
  setError,
  clearCurrentDocument,
  clearRecentDocuments,
} = documentSlice.actions;

/** The slice reducer, registered under the store's `document` key. */
export default documentSlice.reducer;

// HUMAN ASSISTANCE NEEDED
// Consider adding additional actions or thunks for asynchronous operations
// such as fetching documents from an API or saving documents.
// Also, consider implementing error handling for these operations.