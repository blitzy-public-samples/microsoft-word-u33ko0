/**
 * Sign in, sign out and read the current user over HTTP.
 *
 * All three calls use the bare `axios` global rather than the configured instance in
 * `./api.ts`, so none of them carries the base URL or the bearer interceptor.
 * `RootState` is imported and never used.
 *
 * None of the three paths matches a committed server route. The server exposes
 * `POST /token`, `POST /register` and `GET /me`, and this module calls
 * `/auth/login`, `/auth/logout` and `/auth/me`.
 *
 * `axios` is imported and `frontend/package.json` does not declare it.
 *
 * @see ./README.md
 */
import axios from 'axios';
import { RootState } from '../store';
import { User } from '../schema/user';

/**
 * Exchange an email address and password for an access token.
 *
 * The response field read below is `accessToken`, and the server answers
 * `access_token`, so the stored value would be `undefined`. The token is written to
 * `localStorage`, which is readable by any script on the origin.
 *
 * @param email - The submitted address. The server's token route expects a form
 * body with `username`, not a JSON body with `email`.
 * @param password - The submitted password.
 * @returns A promise for the token string.
 * @throws Error with the message `Login failed`, which replaces the server's own
 * status and detail.
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
 * Sign out and clear the stored token.
 *
 * @returns A promise that resolves once the request settles. A failure is logged
 * and swallowed, and the stored token is then left in place, so the caller keeps a
 * usable credential after an apparently completed sign-out.
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
 * Read the signed-in user's profile.
 *
 * @returns A promise for the profile. The response body is cast to `User` with no
 * runtime check, so a mismatched shape passes silently even though
 * `schema/user.ts` declares a schema that could parse it.
 * @throws Error with the message `Failed to fetch current user`.
 */
export const getCurrentUser = async (): Promise<User> => {
  try {
    const response = await axios.get('/auth/me');
    return response.data as User;
  } catch (error) {
    throw new Error('Failed to fetch current user');
  }
};