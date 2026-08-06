/**
 * Hold the client's local view of the current user and the session flags in a Redux Toolkit slice.
 *
 * @remarks
 * The slice is user interface state, not an authentication control. `setUser` assigns
 * `isAuthenticated` the literal `true` without inspecting a token or calling the server, so any
 * caller with a `dispatch` handle can put an arbitrary `User` into the store and raise the flag.
 * Read the flag for rendering only, never as an authorization check. Authentication lives on the
 * server, where `backend/app/api/auth.py` decodes the bearer token for every protected route.
 *
 * The module publishes four action creators and the slice reducer as a default export. Every
 * reducer mutates an Immer draft and returns nothing. Both imports resolve, unlike the matching
 * `Document` import in `store/documentSlice.ts`.
 *
 * Consumers import two names absent here. `pages/Settings.tsx` imports `updateUser`, and four
 * sites import `selectCurrentUser`. The assistance marker below records both gaps.
 * `store/index.ts` imports `{ userReducer }` against the default export, which raises TS2614.
 *
 * @see ./README.md for the store-level register of these findings.
 */
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { User } from '../schema/user';

/** Shape of the user slice state. */
interface UserState {
  currentUser: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

/** Starting state: nobody signed in, unauthenticated, idle and error-free. */
const initialState: UserState = {
  currentUser: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

/**
 * Define the `user` slice and its four reducers.
 *
 * @remarks Each reducer mutates the draft state through Immer, which Redux Toolkit applies.
 *
 * - `setUser` takes a `User`, stores it, sets `isAuthenticated` true, and clears both
 *   `isLoading` and `error`.
 * - `clearUser` drops the user, sets `isAuthenticated` false, and clears the other two fields.
 * - `setLoading` takes a boolean and replaces `isLoading`.
 * - `setError` takes a string, stores it, and clears `isLoading`.
 *
 * `setError` accepts no null, so clearing a message without signing in or out is not possible
 * through these four reducers.
 */
const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    /**
     * Store a user object locally and set the slice's `isAuthenticated` flag to `true`.
     *
     * @param state - Draft `UserState`.
     * @param action - Action whose `payload` is a `User`, the type inferred from `UserSchema`. That
     * shape declares seven fields, `full_name` alone optional, and no `name` field, which
     * `pages/Home.tsx` reads off `currentUser`.
     * @returns Nothing. The reducer assigns `currentUser`, raises `isAuthenticated`, lowers
     * `isLoading` and clears `error`.
     * @remarks The payload is never validated against `UserSchema`, and no token is read, as the
     * module header records.
     * @example
     * ```typescript
     * const action = setUser({ id: 'u-1', email: 'ada@example.com', username: 'ada',
     *   created_at: new Date(), is_active: true, is_superuser: false });
     * // action.type === 'user/setUser'
     * ```
     */
    setUser: (state, action: PayloadAction<User>) => {
      state.currentUser = action.payload;
      state.isAuthenticated = true;
      state.isLoading = false;
      state.error = null;
    },
    /**
     * Reset the user slice to its signed-out state.
     *
     * @param state - Draft `UserState`. The reducer declares no `action` parameter, so it reads no
     * payload.
     * @returns Nothing. The four assignments restore the module-private `initialState`.
     * @remarks `setUser` and `clearUser` are the two reducers that clear `error`. `setError`
     * declares a `string` payload and accepts no `null`, so no dispatch of it can clear the field.
     */
    clearUser: (state) => {
      state.currentUser = null;
      state.isAuthenticated = false;
      state.isLoading = false;
      state.error = null;
    },
    /**
     * Set the loading flag from the boolean payload.
     *
     * @param state - Draft `UserState`.
     * @param action - Action whose `payload` is a `boolean`, assigned to `isLoading`.
     * @returns Nothing. `currentUser`, `isAuthenticated` and `error` stay unchanged.
     */
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    /**
     * Record an error message and stop the loading state.
     *
     * @param state - Draft `UserState`.
     * @param action - Action whose `payload` is a `string`, assigned to `error`.
     * @returns Nothing. The reducer also sets `isLoading` to `false`.
     * @remarks The declared payload is narrower than the `string | null` in
     * `store/documentSlice.ts`, so no value dispatched here returns `error` to `null`.
     */
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isLoading = false;
    },
  },
});

/**
 * Export the four action creators generated from the reducers above.
 *
 * @remarks Each creator returns a plain action whose `type` carries the `user/` prefix from the
 * slice name. No module imports any of the four, because every consumer reaches for
 * `selectCurrentUser` or `updateUser` instead.
 *
 * No dispatch can execute today, because `store/index.ts` imports reducer names the slices never
 * export, so the store cannot construct.
 * @example
 * ```typescript
 * dispatch(setLoading(true));
 * dispatch(setError('Sign-in failed'));
 * dispatch(clearUser());
 * ```
 */
export const { setUser, clearUser, setLoading, setError } = userSlice.actions;

/**
 * The slice reducer, exported as the module default for the store's `user` key.
 *
 * @remarks `store/index.ts` imports the name `userReducer` instead of this default, which is one of
 * the repository's two TS2614 errors.
 */
export default userSlice.reducer;

// HUMAN ASSISTANCE NEEDED
// The following improvements might be needed for production readiness:
// 1. Add more specific error handling and types
// 2. Implement additional user-related actions if required (e.g., updateUser)
// 3. Consider adding selectors for easier state access
// 4. Implement middleware for async operations if needed