/**
 * Compose the application's single Redux store, and publish it with the two derived types.
 *
 * @remarks
 * The store never constructs. The two imports below name `documentReducer` and `userReducer`,
 * while both slices export their reducer as the default: `documentSlice.ts:L52` exports
 * `documentSlice.reducer`, and `userSlice.ts:L45` exports `userSlice.reducer`. Those two
 * imports carry the repository's only two `TS2614` errors.
 *
 * The reducer map registers two keys, `document` and `user`, and no `auth` key, which
 * `services/api.ts:L16` reads as `(store.getState() as RootState).auth.token`.
 *
 * Seven modules import `useAppSelector` or `useAppDispatch` from here: `pages/Editor.tsx:L7`,
 * `pages/Settings.tsx:L5`, `pages/Templates.tsx:L5`, `pages/Home.tsx:L5`,
 * `components/Header.tsx:L3`, `components/DocumentCanvas.tsx:L3` and `components/Toolbar.tsx:L3`.
 * The module defines neither hook, and imports nothing from `react-redux`.
 *
 * @see ./README.md for the store-level register of these findings.
 */

import { configureStore } from '@reduxjs/toolkit';
import { documentReducer } from './documentSlice';
import { userReducer } from './userSlice';

/**
 * Configure the store with the document and user reducers, and expose it as the module default.
 *
 * @remarks
 * The call passes `reducer` alone, with no `middleware`, `devTools`, `preloadedState` or
 * `enhancers` option, and registers exactly two keys, `document` and `user`. The `.auth.token`
 * read at `services/api.ts:L16` therefore resolves against a key this map never declares.
 *
 * `index.tsx:L5` imports the default correctly, as `import store from '@/store'`. `App.tsx:L10`
 * imports `{ store }` from `@/store/index`, a named import of a symbol this module exports
 * only as the default.
 *
 * No consumer can construct this store today, because the two reducer imports above resolve to no
 * exported symbol.
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
 * @remarks
 * Three service modules import this type, `services/api.ts:L2`, `services/auth.ts:L2` and
 * `services/collaboration.ts:L2`, and only `services/api.ts:L16` references it. The `.auth`
 * access there names a reducer key the store never registers, so this type carries no such
 * property.
 */
export type RootState = ReturnType<typeof store.getState>;

/**
 * Describe the type of the store's `dispatch` function.
 *
 * @remarks
 * No module imports this type. The four `useAppDispatch()` call sites, `pages/Editor.tsx:L14`,
 * `pages/Settings.tsx:L13`, `components/DocumentCanvas.tsx:L11` and `components/Toolbar.tsx:L11`,
 * call a hook this module does not export.
 */
export type AppDispatch = typeof store.dispatch;

export default store;