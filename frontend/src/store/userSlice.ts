/** Manage the signed-in user and session flags.
 *
 * Consumers expect updateUser and selectCurrentUser, which this module does not export.
 * The assistance marker at the end of this file records the missing update action and
 * selectors.
 * The slice stores local user-interface state, not authenticated identity. Any caller can
 * dispatch setUser without presenting a token, so isAuthenticated is not an access control.
 */
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { User } from '../schema/user';

/** The signed-in user, the authentication flag, and the status flags. */
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

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    /**
     * Store the signed-in user and open the session.
     *
     * @param state - The user slice state.
     * @param action - Action whose payload is the signed-in user.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    setUser: (state, action: PayloadAction<User>) => {
      state.currentUser = action.payload;
      state.isAuthenticated = true;
      state.isLoading = false;
      state.error = null;
    },
    /**
     * Drop the signed-in user and close the session.
     *
     * @param state - The user slice state.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    clearUser: (state) => {
      state.currentUser = null;
      state.isAuthenticated = false;
      state.isLoading = false;
      state.error = null;
    },
    /**
     * Set the loading flag.
     *
     * @param state - The user slice state.
     * @param action - Action whose payload is the new flag value.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    /**
     * Record an error message and stop the loading state.
     *
     * setUser and clearUser both clear error; setError cannot accept null.
     *
     * @param state - The user slice state.
     * @param action - Action whose payload is the error message.
     * @returns Nothing. Redux Toolkit applies the draft mutation.
     */
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isLoading = false;
    },
  },
});

/**
 * The slice's action creators.
 *
 * @example
 * dispatch(setUser(user));
 */
export const { setUser, clearUser, setLoading, setError } = userSlice.actions;
/** The slice reducer, registered under the store's `user` key. */
export default userSlice.reducer;

// HUMAN ASSISTANCE NEEDED
// The following improvements might be needed for production readiness:
// 1. Add more specific error handling and types
// 2. Implement additional user-related actions if required (e.g., updateUser)
// 3. Consider adding selectors for easier state access
// 4. Implement middleware for async operations if needed