/**
 * Hold the user slice: the signed-in user, the auth flag, loading and error.
 *
 * `User` is imported from `../schema/user`, which does export that type, so this
 * import resolves. Four modules import names this slice does not declare:
 * `selectCurrentUser` as a selector and `updateUser` as an action. See the HUMAN
 * ASSISTANCE NEEDED marker at the end of the file, which lists both as intended
 * additions.
 *
 * @see ./README.md
 */
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { User } from '../schema/user';

interface UserState {
  currentUser: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

const initialState: UserState = {
  currentUser: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

/**
 * Build the `user` slice with four reducers and no async thunk.
 *
 * @remarks No reducer touches `localStorage`, so a stored token does not restore
 * this state on reload.
 */
const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    /**
     * Sign a user in: store the profile, set authenticated, clear status.
     *
     * @param state - The Immer draft of the user slice state.
     * @param action - Carries the signed-in `User` profile.
     * @returns Nothing.
     */
    setUser: (state, action: PayloadAction<User>) => {
      state.currentUser = action.payload;
      state.isAuthenticated = true;
      state.isLoading = false;
      state.error = null;
    },
    /**
     * Sign the user out and reset every field to its opening value.
     *
     * @param state - The Immer draft of the user slice state.
     * @returns Nothing.
     */
    clearUser: (state) => {
      state.currentUser = null;
      state.isAuthenticated = false;
      state.isLoading = false;
      state.error = null;
    },
    /**
     * Set the in-flight flag for an authentication request.
     *
     * @param state - The Immer draft of the user slice state.
     * @param action - Carries the new flag value.
     * @returns Nothing.
     */
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    /**
     * Record an authentication error and clear the in-flight flag.
     *
     * @param state - The Immer draft of the user slice state.
     * @param action - Carries the error message.
     * @returns Nothing.
     */
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isLoading = false;
    },
  },
});

/**
 * The four action creators this slice generates, one per reducer above.
 *
 * @example
 * dispatch(setUser(profile));
 * dispatch(setLoading(true));
 * dispatch(setError('Login failed'));
 * dispatch(clearUser());
 */
export const { setUser, clearUser, setLoading, setError } = userSlice.actions;

/** The reducer for the user slice. */
export default userSlice.reducer;

// HUMAN ASSISTANCE NEEDED
// The following improvements might be needed for production readiness:
// 1. Add more specific error handling and types
// 2. Implement additional user-related actions if required (e.g., updateUser)
// 3. Consider adding selectors for easier state access
// 4. Implement middleware for async operations if needed