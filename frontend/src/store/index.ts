/**
 * Compose the Redux store from the document and user slices.
 *
 * Both reducers are imported by name and both slice modules export their reducer as
 * a default, so each import resolves to `undefined`. The store therefore registers
 * two undefined reducers under `document` and `user`.
 *
 * Seven modules import `useAppSelector` or `useAppDispatch` from here, and this
 * module declares neither. `services/api.ts` reads `state.auth.token`, and no
 * `auth` key is registered.
 *
 * @see ./README.md
 */
import { configureStore } from '@reduxjs/toolkit';
import { documentReducer } from './documentSlice';
import { userReducer } from './userSlice';

/**
 * The application store, exported as this module's default at the end of the file.
 *
 * @remarks `App.tsx` imports it by name, which does not resolve. `index.tsx`
 * imports the default, which does.
 */
const store = configureStore({
  reducer: {
    document: documentReducer,
    user: userReducer,
  },
});

/** The shape of the whole store state, inferred from `store.getState`. */
export type RootState = ReturnType<typeof store.getState>;
/** The dispatch type of this store, including any configured middleware. */
export type AppDispatch = typeof store.dispatch;

export default store;