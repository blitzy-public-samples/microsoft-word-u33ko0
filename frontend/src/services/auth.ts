/** Call the three authentication endpoints and hold the access token in local storage.
 *
 * `login` and `logout` write and clear the token in `localStorage`, and `getCurrentUser` reads the
 * signed-in user. The server issues a JSON Web Token (JWT), treated here as an opaque string. No
 * module under `frontend/src` imports this file, so nothing in the application calls the three.
 *
 * The token never reaches Redux. `login` writes `localStorage['accessToken']`, no code copies that
 * value into the store, and `frontend/src/services/api.ts` reads `auth.token` from Redux for its
 * `Authorization` header, so the writer here and that reader share no state.
 *
 * Every function calls the unconfigured default Axios export rather than the configured instance
 * in `api.ts`, so
 * each request skips that module's base URL and its bearer-token interceptor. `axios` is absent
 * from `frontend/package.json`, which raises one TS2307. `RootState` resolves and is unused.
 *
 * Nothing gives those relative paths an API origin. `frontend/package.json` declares no
 * `proxy` key, so the Create React App development server forwards nothing to the backend.
 * `infrastructure/docker/frontend.Dockerfile:L26` leaves the custom Nginx configuration `COPY`
 * commented out, so the production image proxies nothing either.
 *
 * Each request therefore targets the origin serving the bundle. That origin is the development
 * server under `npm start` and the Nginx container under Docker. The backend listens on a
 * different origin in both cases, so every request here reaches the frontend rather than the
 * application programming interface.
 *
 * `axios` is absent from `frontend/package.json`, whose `dependencies` block spans L6-L14 and
 * names seven packages, so L68 raises one TS2307 error.
 *
 * L69 imports `RootState` from `../store` and no code here reads the name. The import still
 * resolves, because `frontend/src/store/index.ts:L54` exports the type. L70 imports `User` from
 * `../schema/user`, and that import resolves as well, because
 * `frontend/src/schema/user.ts:L56` declares `export type User = z.infer<typeof UserSchema>`.
 * Neither line is an error. The sibling module `frontend/src/schema/document.ts` omits the
 * equivalent alias, which is why `api.ts` and `collaboration.ts` fail on their schema imports
 * and this module does not.
 *
 * None of the three request paths reaches a committed server route. The client calls
 * `/auth/login` (L146), `/auth/logout` (L194) and `/auth/me` (L239). The server exposes
 * `POST /token` (`backend/app/api/auth.py:L170`), `POST /register`
 * (`backend/app/api/auth.py:L245`) and `GET /me` (`backend/app/api/users.py:L32`).
 * `backend/app/main.py:L125-L128` mounts all four routers with no prefix, so the server answers
 * those three paths at the root. No logout route exists anywhere in the backend, which leaves
 * `/auth/logout` with no counterpart at all rather than a differently named one.
 *
 * `GET /me` is registered and still unreachable, so renaming this module's path would not
 * reach it. `backend/app/main.py:L126` mounts the documents router before `:L51` mounts the
 * users router, and `GET /{document_id}` at `backend/app/api/documents.py:L148` compiles to the
 * same single-segment pattern that `/me` occupies. Starlette matches path templates in
 * registration order, so a request to `/me` arrives at the document get-one handler with
 * `document_id` bound to the literal string `me`. `PUT /me` at `backend/app/api/users.py:L53`
 * is shadowed the same way, by `PUT /{document_id}` at `backend/app/api/documents.py:L191`.
 * Both profile routes are therefore registered and unreachable through the assembled route
 * order, and only the token route and the register route answer as their authors intended.
 *
 * The specification matches this client and not the server.
 * `documentation/Technical Specifications.md`, under its `API DESIGN` heading, declares an
 * `/auth` group holding `POST /login` and `POST /logout`. That same heading declares
 * `GET /users/me`, so the profile path exists in three forms: `/users/me` in the
 * specification, `/me` on the server and `/auth/me` in this client.
 *
 * No module under `frontend/src` imports this file. The only service imports are three of
 * `services/api`, at `frontend/src/pages/Editor.tsx:L25`,
 * `frontend/src/pages/Settings.tsx:L31` and `frontend/src/pages/Templates.tsx:L35`, so nothing
 * in the running application calls `login`, `logout` or `getCurrentUser`.
 *
 * @see ./README.md for the service-level defect register.
 */
import axios from 'axios';
import { RootState } from '../store';
import { User } from '../schema/user';

/**
 * Exchange an email and password for an access token, and store the token locally.
 *
 * @param email - Address sent as the `email` field of the request body.
 * @param password - Secret sent as the `password` field of the request body.
 * @returns The token read from the response body.
 * @remarks Side effect: the token is written to browser `localStorage` under the key
 * `accessToken`, which is the only place it is kept.
 *
 * @remarks L148 writes the token to browser `localStorage` under the key `accessToken`, so the
 * call changes browser storage as well as returning. `localStorage` is readable by any script
 * running on the page's origin, so a cross-site scripting defect anywhere in the application can
 * read the stored value and send it elsewhere. The browser also keeps the key until a script or
 * the user clears it, which outlives the tab. What the write stores today is the string
 * `"undefined"`, described below, so nothing usable leaks yet. Correcting the field name in the
 * next paragraph puts a real bearer credential in that same script-readable slot.
 *
 * No committed line reads the key back. `frontend/src/services/api.ts:L140-L149` builds its bearer
 * header from the Redux store rather than from `localStorage`, so the stored value never reaches
 * an outgoing request.
 *
 * The request contract does not match the server's token route. L146 sends an HTTP POST with a
 * JavaScript object body carrying `email` and `password`, which Axios serializes as JSON under
 * `Content-Type: application/json`. `backend/app/api/auth.py:L171` declares
 * `form_data: OAuth2PasswordRequestForm = Depends()`, and FastAPI populates that dependency
 * only from an `application/x-www-form-urlencoded` body whose identity field is named
 * `username`. Three things differ at once: the path, the body encoding and the identity field
 * name. FastAPI also requires the `python-multipart` package before it can parse any form
 * body, and the repository commits no backend dependency manifest that declares it.
 *
 * L147 reads `response.data.accessToken` in camelCase, and `backend/app/api/auth.py:L243` returns
 * `{"access_token": ..., "token_type": "bearer"}` in snake_case. The read therefore yields
 * `undefined`, L148 stores the string `"undefined"` under the key, and L149 returns `undefined` to
 * the caller. No error accompanies any of those three steps.
 *
 * The stored token has no reader anywhere in the frontend. No module under `frontend/src`
 * calls `localStorage.getItem('accessToken')`, and no module dispatches the returned value
 * into the Redux store. The one place that attaches a bearer header,
 * `frontend/src/services/api.ts:L142`, reads `store.getState().auth.token` instead, and
 * `frontend/src/store/index.ts:L42-L45` registers no `auth` reducer key for it to read.
 * Correcting the field name at L147 fixes the stored value and leaves the flow disconnected,
 * because the writer and the reader use different stores.
 *
 * Browser `localStorage` is script-readable, same-origin, persistent storage. Any script on
 * the page origin can read this key through the same interface L148 writes with. The value also
 * survives a tab close and a browser restart, until some line removes it.
 *
 * Nothing here narrows that exposure, in three separate ways. No `httpOnly` cookie and no
 * in-memory holder is used as an alternative. No line reads the token's `exp` claim, so
 * storage and token lifetime are never synchronized and an expired token stays readable. No
 * `storage` event listener exists, so a sign-out in one tab leaves every other tab holding its
 * own view of the key.
 *
 * L150-L13 catch every failure and throw `new Error('Login failed')` at L151 without attaching
 * the original error. A rejected credential and a dropped connection reach the caller as the
 * same message.
 *
 * Resilience is absent, and every absence belongs to the application rather than to the
 * library. L146 calls the unconfigured default Axios export with no `timeout`, no `signal` and no
 * `AbortController`, and no retry, backoff, jitter, circuit breaker or fallback surrounds it.
 * L151 discards the original error, so a caller cannot read a status code to decide whether a
 * retry is even appropriate. `axios` is absent from `frontend/package.json` and no lockfile is
 * committed, so this repository fixes no library version and supports no claim about the
 * library's own default behavior.
 *
 * @example
 * const token = await login('user@example.com', '<password>');
 * // The placeholder stands in for a secret the caller supplies at run time. Examples in this
 * // repository carry no real credential and no value that a policy would accept.
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
 * Notify the server of a sign-out and clear the stored access token.
 *
 * @returns A promise that resolves once the request settles, per the declared `Promise<void>`.
 * @remarks Side effect: the `accessToken` key is removed from `localStorage`, and only after the
 * request resolves, so a failed request leaves the token in browser storage.
 *
 * @remarks L194 issues the request and L195 removes the `accessToken` key from `localStorage`.
 * L195 runs only after L194 resolves, so a failed request leaves the token in browser storage.
 *
 * The failure path differs from the other two functions in this module. L196-L22 catch the
 * error, L197 logs it through `console.error('Logout failed', error)`, and no line rethrows. A
 * failed logout therefore resolves rather than rejects, and the caller sees success either way.
 *
 * The two behaviors above combine into token retention. No committed server route answers
 * `POST /auth/logout`, so L194 rejects in practice, L195 never runs, and L197 writes to the
 * console while the promise resolves. The script-readable, persistent value that `login`
 * stored therefore stays in `localStorage` after a caller believes the session ended, and no
 * line removes it unconditionally in a `finally` block.
 *
 * L197 logs the whole error object rather than a message. An Axios error carries `config`,
 * `request` and `response`, so the browser console can end up holding the request URL, the
 * request headers, the request body and the response body for the failed call. Anything with
 * access to that console, including a browser extension or a support tool that collects logs,
 * reads whatever those fields held.
 *
 * Resilience is absent here for the same reasons recorded on `login`. L194 calls the
 * unconfigured default Axios export with no `timeout`, no `signal` and no
 * `AbortController`, and no retry,
 * backoff, jitter, circuit breaker or fallback surrounds it. L197 keeps the original error in
 * the console only, so no caller and no monitor can act on it.
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
 * Fetch the signed-in user's profile.
 *
 * @returns The response body cast to `User`, a shape carrying `id`, `email`, `username`, optional
 * `full_name`, `created_at`, `is_active` and `is_superuser`.
 * @remarks The cast is unchecked. `response.data as User` validates nothing, so a body of any
 * shape passes and a mismatch surfaces wherever a caller reads a field. `UserSchema` sits in the
 * same module as the type and is never applied.
 *
 * The `User` type declares neither `name` nor `avatar`, and `frontend/src/components/Header.tsx`
 * and `frontend/src/pages/Home.tsx` both read those fields from a user object.
 *
 * The `User` type at `frontend/src/schema/user.ts:L56` declares neither `name` nor `avatar`,
 * which `frontend/src/components/Header.tsx` and `frontend/src/pages/Home.tsx` both read from a
 * user object.
 *
 * L239 sends no credential of any kind. The request skips the bearer-token interceptor that
 * `frontend/src/services/api.ts:L140-L149` installs, and no line here reads the `accessToken`
 * key that `login` wrote, so the profile request carries no `Authorization` header. A server
 * route guarded by `Depends(get_current_user)` would reject it before reaching any handler.
 *
 * L241-L31 throw `new Error('Failed to fetch current user')` at L242 without attaching the
 * original error, so the caller cannot separate a missing route from a rejected token.
 *
 * Resilience is absent here for the same reasons recorded on `login`. L239 calls the
 * unconfigured default Axios export with no `timeout`, no `signal` and no
 * `AbortController`, and no retry,
 * backoff, jitter, circuit breaker or fallback surrounds it. L242 discards the original error.
 *
 * @example
 * const user = await getCurrentUser();
 * // Cannot run today: `axios` is absent from frontend/package.json, and no reachable server
 * // route answers this request. The nearest registered route is GET /me at
 * // backend/app/api/users.py:L32, and the header above records why the assembled route order
 * // leaves that one unreachable too.
 */
export const getCurrentUser = async (): Promise<User> => {
  try {
    const response = await axios.get('/auth/me');
    return response.data as User;
  } catch (error) {
    throw new Error('Failed to fetch current user');
  }
};