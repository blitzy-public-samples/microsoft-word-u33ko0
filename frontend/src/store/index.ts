/** Configure the Redux store and export its state and dispatch types.
 *
 * @reduxjs/toolkit is declared in frontend/package.json, so configureStore resolves.
 * The named reducer imports and the hooks expected by consumers are unresolved.
 */
import { configureStore } from '@reduxjs/toolkit';
import { documentReducer } from './documentSlice';
import { userReducer } from './userSlice';

/**
 * The configured store, holding the `document` and `user` reducer keys.
 */
const store = configureStore({
  reducer: {
    document: documentReducer,
    user: userReducer,
  },
});

/**
 * The shape of the whole store state, inferred from `store.getState`.
 */
export type RootState = ReturnType<typeof store.getState>;

/**
 * The dispatch type of the configured store.
 */
export type AppDispatch = typeof store.dispatch;

export default store;