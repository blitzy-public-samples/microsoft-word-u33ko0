/**
 * Hold the signed-in user and the session flags in a Redux Toolkit slice.
 *
 * @remarks
 * L44 publishes four action creators, `setUser`, `clearUser`, `setLoading` and `setError`, and L45
 * exports the slice reducer as the default. Both imports below resolve, and the module names no
 * undeclared package: `frontend/package.json:L7` declares `@reduxjs/toolkit` at `^1.9.5`, and
 * `schema/user.ts:L13` exports `type User`. The matching import at `store/documentSlice.ts:L2`
 * fails, because `schema/document.ts` exports two Zod schemas and no inferred type.
 *
 * Consumers import two names absent here. `pages/Settings.tsx:L6` imports `updateUser`, and four
 * sites import `selectCurrentUser`: `pages/Settings.tsx:L6`, `pages/Templates.tsx:L6`,
 * `pages/Home.tsx:L6` and `components/Header.tsx:L4`. The assistance marker at L47 records both
 * gaps. `store/index.ts:L3` imports `{ userReducer }` as a named symbol against the default export
 * at L45, so `tsc` reports `TS2614` there.
 *
 * @see ./README.md for the store-level register of these findings.
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

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    /**
     * Record the signed-in user and mark the session authenticated.
     *
     * @param state - Draft `UserState`, the module-private shape at L4-L9.
     * @param action - Action whose `payload` is a `User`, the type `schema/user.ts:L13` infers from
     * `UserSchema`. The shape declares seven fields at `schema/user.ts:L3-L11`, and `full_name` is
     * the only optional one. The shape omits a `name` field, which `pages/Home.tsx:L16` reads off
     * `currentUser`.
     * @remarks
     * The reducer changes four fields, and only the first stores the user. L23 assigns
     * `currentUser` from the payload, L24 sets `isAuthenticated` to `true`, L25 sets `isLoading` to
     * `false`, and L26 sets `error` to `null`.
     *
     * The reducer returns nothing. Redux Toolkit hands the reducer an Immer draft. Immer commits
     * the four assignments as the next state, so the effect is a mutation, not a return value.
     * @example
     * ```typescript
     * const action = setUser({ id: 'u-1', email: 'ada@example.com', username: 'ada',
     *   created_at: new Date(), is_active: true, is_superuser: false });
     * // action.type === 'user/setUser', from the slice name at L19
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
     * @param state - Draft `UserState`, the module-private shape at L4-L9. The reducer declares no
     * `action` parameter, so it reads no payload.
     * @remarks
     * L29 sets `currentUser` to `null`, L30 sets `isAuthenticated` to `false`, L31 sets `isLoading`
     * to `false`, and L32 sets `error` to `null`, which restores the module-private `initialState`
     * at L11-L16.
     *
     * `clearUser` is the only reducer here that clears `error`, because `setError` at L37 declares
     * a `string` payload and accepts no `null`.
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
     * @param state - Draft `UserState`, the module-private shape at L4-L9.
     * @param action - Action whose `payload` is a `boolean`, assigned to `isLoading` at L35.
     * @remarks
     * L35 is the only assignment, so `currentUser`, `isAuthenticated` and `error` stay unchanged.
     */
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    /**
     * Record an error message and stop the loading state.
     *
     * @param state - Draft `UserState`, the module-private shape at L4-L9.
     * @param action - Action whose `payload` is a `string`, assigned to `error` at L38.
     * @remarks
     * The reducer changes two fields. L38 assigns `error` from the payload, and L39 sets
     * `isLoading` to `false`.
     *
     * The declared payload is `string`, narrower than the `string | null` at
     * `store/documentSlice.ts:L31`, so no value dispatched here returns `error` to `null`. Only
     * `clearUser` at L28 clears the field.
     */
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isLoading = false;
    },
  },
});

/**
 * Publish the four action creators `createSlice` derives from the reducers above.
 *
 * @remarks
 * The `createSlice` call at L18 generates one creator per reducer key, so the destructuring below
 * exports `setUser`, `clearUser`, `setLoading` and `setError`. Each creator returns a plain action
 * whose `type` carries the `user/` prefix from the slice name at L19.
 *
 * No module imports any of the four. Every consumer of this slice reaches for `selectCurrentUser`
 * or `updateUser` instead, and the file header above cites those import sites.
 *
 * No dispatch can execute today, because `store/index.ts:L2-L3` imports reducer names the slices
 * never export, so the store cannot construct.
 * @example
 * ```typescript
 * dispatch(setLoading(true));
 * dispatch(setError('Sign-in failed'));
 * dispatch(clearUser());
 * ```
 */
export const { setUser, clearUser, setLoading, setError } = userSlice.actions;
export default userSlice.reducer;

// HUMAN ASSISTANCE NEEDED
// The following improvements might be needed for production readiness:
// 1. Add more specific error handling and types
// 2. Implement additional user-related actions if required (e.g., updateUser)
// 3. Consider adding selectors for easier state access
// 4. Implement middleware for async operations if needed