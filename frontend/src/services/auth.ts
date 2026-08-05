/** Wrap the three authentication calls and hold the browser's access token.
 *
 * `login` and `logout` write and clear the token in `localStorage`, and `getCurrentUser` reads
 * the signed-in user. The server issues a JSON Web Token (JWT), which every function here
 * treats as an opaque string.
 *
 * Line numbers below refer to the committed file, before this header existed.
 *
 * L1 imports the bare `axios` default global rather than the configured instance that
 * `frontend/src/services/api.ts:L7` builds. Every request here skips that module's base URL
 * (`api.ts:L9`) and its bearer-token request interceptor (`api.ts:L14-L23`). Each request
 * travels to a relative path against whatever origin serves the page.
 *
 * `axios` is absent from `frontend/package.json`, whose `dependencies` block spans L6-L14 and
 * names seven packages, so L1 raises one TS2307 error.
 *
 * L2 imports `RootState` from `../store` and no code here reads the name. The import still
 * resolves, because `frontend/src/store/index.ts:L12` exports the type. L3 imports `User` from
 * `../schema/user`, and that import resolves as well, because
 * `frontend/src/schema/user.ts:L13` declares `export type User = z.infer<typeof UserSchema>`.
 * Neither line is an error. The sibling module `frontend/src/schema/document.ts` omits the
 * equivalent alias, which is why `api.ts` and `collaboration.ts` fail on their schema imports
 * and this module does not.
 *
 * None of the three request paths reaches a committed server route. The client calls
 * `/auth/login` (L7), `/auth/logout` (L18) and `/auth/me` (L27). The server exposes
 * `POST /token` (`backend/app/api/auth.py:L28`), `POST /register`
 * (`backend/app/api/auth.py:L42`) and `GET /me` (`backend/app/api/users.py:L8`).
 * `backend/app/main.py:L49-L52` mounts all four routers with no prefix, so the server answers
 * those three paths at the root. No logout route exists anywhere in the backend, which leaves
 * `/auth/logout` with no counterpart at all rather than a differently named one.
 *
 * The specification matches this client and not the server.
 * `documentation/Technical Specifications.md`, under its `API DESIGN` heading, declares an
 * `/auth` group holding `POST /login` and `POST /logout`. That same heading declares
 * `GET /users/me`, so the profile path exists in three forms: `/users/me` in the
 * specification, `/me` on the server and `/auth/me` in this client.
 *
 * No module under `frontend/src` imports this file. The only service imports are three of
 * `services/api`, at `frontend/src/pages/Editor.tsx:L6`,
 * `frontend/src/pages/Settings.tsx:L4` and `frontend/src/pages/Templates.tsx:L4`, so nothing
 * in the running application calls `login`, `logout` or `getCurrentUser`.
 */

import axios from 'axios';
import { RootState } from '../store';
import { User } from '../schema/user';

/**
 * Post the supplied credentials to `/auth/login` and store the token from the response.
 *
 * @param email - Address sent as the `email` field of the request body.
 * @param password - Secret sent as the `password` field of the request body.
 * @returns The value L8 reads from the response body, returned at L10.
 *
 * @remarks L9 writes the token to browser `localStorage` under the key `accessToken`, so the
 * call changes browser storage as well as returning.
 *
 * L8 reads `response.data.accessToken` in camelCase, and `backend/app/api/auth.py:L40` returns
 * `{"access_token": ..., "token_type": "bearer"}` in snake_case. The read therefore yields
 * `undefined`, L9 stores the string `"undefined"` under the key, and L10 returns `undefined` to
 * the caller. No error accompanies any of those three steps.
 *
 * L11-L13 catch every failure and throw `new Error('Login failed')` at L12 without attaching
 * the original error. A rejected credential and a dropped connection reach the caller as the
 * same message.
 *
 * @example
 * const token = await login('user@example.com', 'a-password');
 * // Cannot run today: `axios` is absent from frontend/package.json, and no committed server
 * // route answers POST /auth/login.
 */
export const login = async (email: string, password: string): Promise<string> => {
  try {
    const response = await axios.post('/auth/login', { email, password });
    const accessToken = response.data.accessToken;
    localStorage.setItem('accessToken', accessToken);
    return accessToken;
  } catch (error) {
    throw new Error('Login failed');
  }
};

/**
 * Post to `/auth/logout` and clear the stored token.
 *
 * @returns A promise that resolves once the request settles, per the declared `Promise<void>`.
 *
 * @remarks L18 issues the request and L19 removes the `accessToken` key from `localStorage`.
 * L19 runs only after L18 resolves, so a failed request leaves the token in browser storage.
 *
 * The failure path differs from the other two functions in this module. L20-L22 catch the
 * error, L21 logs it through `console.error('Logout failed', error)`, and no line rethrows. A
 * failed logout therefore resolves rather than rejects, and the caller sees success either way.
 *
 * @example
 * await logout();
 * // Cannot run today: `axios` is absent from frontend/package.json, and the backend declares
 * // no logout route at all.
 */
export const logout = async (): Promise<void> => {
  try {
    await axios.post('/auth/logout');
    localStorage.removeItem('accessToken');
  } catch (error) {
    console.error('Logout failed', error);
  }
};

/**
 * Fetch the signed-in user from `/auth/me`.
 *
 * @returns The response body cast to `User`, a shape carrying `id`, `email`, `username`,
 * optional `full_name`, `created_at`, `is_active` and `is_superuser`.
 *
 * @remarks L28 casts `response.data` with `as User` and validates nothing. A body of any shape
 * passes that cast, so a mismatch surfaces later wherever a caller reads a field, not at L28.
 * `UserSchema` sits in the same module as the type, at `frontend/src/schema/user.ts:L3`, and no
 * line here applies it.
 *
 * The `User` type at `frontend/src/schema/user.ts:L13` declares neither `name` nor `avatar`,
 * which `frontend/src/components/Header.tsx` and `frontend/src/pages/Home.tsx` both read from a
 * user object.
 *
 * L29-L31 throw `new Error('Failed to fetch current user')` at L30 without attaching the
 * original error, so the caller cannot separate a missing route from a rejected token.
 *
 * @example
 * const user = await getCurrentUser();
 * // Cannot run today: `axios` is absent from frontend/package.json, and the server exposes
 * // GET /me rather than GET /auth/me.
 */
export const getCurrentUser = async (): Promise<User> => {
  try {
    const response = await axios.get('/auth/me');
    return response.data as User;
  } catch (error) {
    throw new Error('Failed to fetch current user');
  }
};