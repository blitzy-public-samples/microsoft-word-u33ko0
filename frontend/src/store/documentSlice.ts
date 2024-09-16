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
    setCurrentDocument: (state, action: PayloadAction<Document>) => {
      state.currentDocument = action.payload;
    },
    addRecentDocument: (state, action: PayloadAction<Document>) => {
      state.recentDocuments = [action.payload, ...state.recentDocuments.slice(0, 4)];
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
    clearRecentDocuments: (state) => {
      state.recentDocuments = [];
    },
  },
});

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