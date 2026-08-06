/**
 * Compose the Redux store from the document and user slices, and export its two types.
 *
 * Both reducer imports are named, while each slice exports its reducer only as the default,
 * so neither name resolves and the store cannot construct. `App.tsx` mirrors the same fault
 * in the other direction, importing `{ store }` from a module that exports it as the default.
 *
 * The store never constructs. The imports below name `documentReducer` and `userReducer`, while
 * both slices export their reducer as the default, which produces the repository's only two
 * TS2614 errors.
 *
 * The reducer map registers `document` and `user` and no `auth` key, which
 * `frontend/src/services/api.ts` reads as `auth.token` for its `Authorization` header.
 *
 * Seven modules import `useAppSelector` or `useAppDispatch` from here, across the four pages and
 * three of the components. The module defines neither hook and imports nothing from `react-redux`.
 *
 * @see ./README.md for the store-level register of these findings.
 */
import { configureStore } from '@reduxjs/toolkit';
import { documentReducer } from './documentSlice';
import { userReducer } from './userSlice';

/**
 * The single application store, holding the `document` and `user` state trees.
 *
 * @remarks
 * The call passes `reducer` alone, with no `middleware`, `devTools`, `preloadedState` or
 * `enhancers` option, and registers exactly two keys.
 *
 * `index.tsx` imports the default correctly. `App.tsx` imports `{ store }`, a named import of a
 * symbol this module exports only as the default. Neither consumer can construct the store, because
 * the two reducer imports above resolve to no exported symbol.
 * @example
 * ```tsx
 * import store from '@/store';
 *
 * <Provider store={store}>{children}</Provider>
 * ```
 */
const store = configureStore({
  reducer: {
    document: documentReducer,
    user: userReducer,
  },
});

/**
 * Describe the shape of the whole store state, read from the return type of `store.getState`.
 *
 * @remarks Three service modules import this type, and only `services/api.ts` references it, where
 * the `.auth` access names a reducer key the store never registers.
 */
export type RootState = ReturnType<typeof store.getState>;

/**
 * Describe the type of the store's `dispatch` function.
 *
 * @remarks No module imports this type. The four `useAppDispatch()` call sites reach for a hook
 * the module does not export.
 */
export type AppDispatch = typeof store.dispatch;

/** Export the store as this module's default binding. */
export default store;