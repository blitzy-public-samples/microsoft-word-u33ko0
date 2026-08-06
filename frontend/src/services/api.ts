/** Centralize the document REST calls behind a module-private Axios instance.
 *
 * REST abbreviates Representational State Transfer. The three exported functions share one
 * instance that supplies the base URL and both interceptors.
 *
 * Unresolved and mismatched dependencies:
 * - `axios` is imported and absent from `frontend/package.json`, so the import raises TS2307.
 * - `Document`, `DocumentCreate` and `DocumentUpdate` do not exist in `../schema/document`, which
 *   exports `DocumentSchema` and `DocumentVersionSchema` and no inferred type. Three TS2305
 *   errors follow. `RootState` from `../store` does resolve.
 * - `REACT_APP_API_BASE_URL` is the only `process.env` read in the frontend, while
 *   `infrastructure/docker/docker-compose.yml` injects `REACT_APP_API_URL`, so the base URL
 *   resolves to `undefined`.
 * - `getDocument`, `getTemplates` and `updateUserSettings` are imported from this module by the
 *   editor, templates and settings pages, and none of the three is defined here.
 *
 * The request interceptor reads `store.getState()` without importing `store`, then reads an
 * `auth` key the store never registers, so supplying the missing import still leaves a
 * missing slice. The base URL reads `REACT_APP_API_BASE_URL`, while Compose injects
 * `REACT_APP_API_URL`, so the base URL resolves to `undefined`.
 *
 * L80 imports `Document`, `DocumentCreate` and `DocumentUpdate` from `../schema/document`. The
 * path resolves and all three names are absent, because that module exports only the schema
 * values `DocumentSchema` and `DocumentVersionSchema` and declares no `z.infer` alias. Three
 * TS2305 errors follow. L79 imports `RootState` from `../store`, and
 * `frontend/src/store/index.ts:L54` does export it.
 *
 * L142 carries two independent faults, and they surface one after the other. No import brings
 * `store` into this module, so the read raises `ReferenceError` first. Supplying that import
 * exposes the second fault: `frontend/src/store/index.ts:L42-L45` registers only the `document`
 * and `user` reducer keys, so the `auth` key L142 reads does not exist and a `TypeError`
 * follows.
 *
 * L82 reads `REACT_APP_API_BASE_URL`, while `infrastructure/docker/docker-compose.yml:L11`
 * injects `REACT_APP_API_URL`. The two names differ, so the base URL resolves to `undefined`.
 * L82 holds the only `process.env` read in the frontend.
 *
 * The key mismatch is one of seven independent barriers between L82 and a working base URL.
 * Each one blocks the committed Docker deployment on its own, so repairing the key name
 * leaves the other six standing. In the order a deployer meets them:
 *
 * 1. The images do not build. `infrastructure/docker/docker-compose.yml:L5-L7` sets the
 *    frontend build context to `../../frontend` and the Dockerfile to `Dockerfile`, and no
 *    `frontend/Dockerfile` is tracked. The two committed Dockerfiles sit at
 *    `infrastructure/docker/frontend.Dockerfile` and
 *    `infrastructure/docker/backend.Dockerfile`, and `docker-compose.yml:L18-L20` repeats the
 *    same mismatch for the backend service.
 * 2. Build-time substitution. `frontend/package.json:L29` pins `react-scripts` 5.0.1, and
 *    Create React App replaces every `process.env.REACT_APP_*` read with a literal during
 *    `npm run build`. A value supplied after the build cannot reach L82.
 * 3. No build-time value. `infrastructure/docker/frontend.Dockerfile:L17` runs
 *    `npm run build` with no `ARG` and no `ENV` above it, so the literal baked into the
 *    bundle is `undefined`.
 * 4. Runtime injection into the wrong stage.
 *    `infrastructure/docker/docker-compose.yml:L10-L11` sets `REACT_APP_API_URL` on the
 *    running container, which serves the already-built static bundle through Nginx.
 * 5. No API proxy. `frontend/package.json` declares no `proxy` key, and
 *    `infrastructure/docker/frontend.Dockerfile:L26` leaves the custom Nginx configuration
 *    `COPY` commented out, so the served image forwards no request to the backend.
 * 6. Frontend port mismatch. `infrastructure/docker/frontend.Dockerfile:L29` exposes 80 and
 *    `:L32` starts Nginx, which serves port 80, while
 *    `infrastructure/docker/docker-compose.yml:L8-L9` publishes `3000:3000`. Nothing
 *    listens on the container port Compose publishes.
 * 7. Backend port mismatch and host resolution.
 *    `infrastructure/docker/backend.Dockerfile:L17` and `:L20` serve port 8000, while
 *    `infrastructure/docker/docker-compose.yml:L21-L22` publishes `5000:5000`. The value
 *    Compose injects, `http://backend:5000`, names a Compose service, and the browser runs
 *    on the host outside that network, so it resolves no such host.
 *
 * Three symbols other modules import from here never appear in this file: `getDocument`
 * (`frontend/src/pages/Editor.tsx:L25`), `getTemplates`
 * (`frontend/src/pages/Templates.tsx:L35`) and `updateUserSettings`
 * (`frontend/src/pages/Settings.tsx:L31`).
 *
 * @see ./README.md for the service-level defect register.
 */

import axios, { AxiosInstance } from 'axios';
import { RootState } from '../store';
import { Document, DocumentCreate, DocumentUpdate } from '../schema/document';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

/**
 * Build the shared Axios instance, wiring its base URL, default content type and interceptors.
 *
 * @returns The configured `AxiosInstance`.
 * @remarks
 * The symbol carries no `export` keyword, so it stays private to this module, and the default
 * `Content-Type` it sets applies to every request. The response interceptor passes both the
 * response and the error through unchanged.
 *
 * The request interceptor reads `auth.token` from the Redux store and sets `Authorization` to
 * `Bearer <token>` when a value is present. No producer can supply it:
 * `frontend/src/services/auth.ts` writes the token to `localStorage['accessToken']`, nothing
 * copies it into Redux, and `frontend/src/store/index.ts` registers only the `document` and
 * `user` reducer keys.
 *
 * The request interceptor at L140-L23 reads a token and, when one is present, sets the
 * `Authorization` header to `Bearer <token>`. L142 fails twice, and the two failures are
 * sequential rather than simultaneous. No import brings `store` into this module, so the
 * first request raises `ReferenceError: store is not defined`. Supplying that import moves
 * the failure one step along. `frontend/src/store/index.ts:L42-L45` registers only the
 * `document` and `user` reducer keys, so `getState().auth` evaluates to `undefined` and
 * reading `.token` from it raises a `TypeError`. Under either failure the interceptor never
 * reaches the header assignment at L144.
 *
 * No issued token reaches this interceptor even once both faults are repaired, because the
 * writer and the reader use different stores. `frontend/src/services/auth.ts:L148` writes to
 * browser `localStorage` under the key `accessToken`. The value it writes comes from
 * `response.data.accessToken` at `auth.ts:L147`, a camelCase field that
 * `backend/app/api/auth.py:L243` never sends, so the stored string is `"undefined"`. No
 * module under `frontend/src` calls `localStorage.getItem('accessToken')`, and no module
 * dispatches a token into the Redux store, so the path L142 reads has no writer at all. The
 * flow is broken at both ends: the one writer stores a useless value where nothing reads,
 * and the one reader reads where nothing writes. `auth.ts:L194-L195` removes the key only
 * after the logout request resolves, and `auth.ts:L196-L198` swallows the error, so a failed
 * logout keeps the stored value while reporting success.
 *
 * The response interceptor at L151-L31 passes both outcomes straight through: L152 returns the
 * response unchanged and L155 re-rejects the error unchanged. L154 carries the file's only
 * pre-existing comment, inside that error branch.
 *
 * Resilience is absent from this module, and every absence below belongs to the application
 * rather than to the library. `axios.create` at L134-L10 receives `baseURL` alone, so no
 * `timeout`, no `signal` and no `validateStatus` is configured. No `AbortController` and no
 * cancellation token reaches any request. No retry, no backoff, no jitter, no circuit
 * breaker and no fallback response exists anywhere in the module, and L155 re-rejects instead
 * of recovering. `axios` is absent from `frontend/package.json` and no lockfile is committed,
 * so this repository fixes no library version and supports no claim about the library's own
 * default behavior.
 */
const createApiClient = (): AxiosInstance => {
  const instance = axios.create({
    baseURL: API_BASE_URL,
  });

  instance.defaults.headers.common['Content-Type'] = 'application/json';

  instance.interceptors.request.use(
    (config) => {
      const token = (store.getState() as RootState).auth.token;
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      // Handle global error responses here
      return Promise.reject(error);
    }
  );

  return instance;
};

const api = createApiClient();

/**
 * Request the full document list through `GET /documents`.
 *
 * @returns A promise resolving to the Axios `response.data`, typed as `Document[]`.
 * @remarks Every call travels through the shared `api` instance, so the request interceptor
 * runs first and fails at L142. Both rejection handlers propagate the original error
 * unchanged.
 *
 * The `Document[]` in the signature is a compile-time annotation and nothing more. The
 * generic argument at L218 tells the type checker what to expect and emits no code. The three
 * type names L80 imports are absent from `frontend/src/schema/document.ts`, and no line here
 * calls a Zod schema.
 *
 * L219 returns `response.data` exactly as received. A null body, a body of some other shape,
 * and date values arriving as JSON strings where `DocumentSchema` declares `z.date()` at
 * `frontend/src/schema/document.ts:L70-L71` all reach the caller unconverted and unreported.
 *
 * Five layers stand between this call and a document list, and each one blocks on its own.
 * Repairing any single layer leaves the rest standing. In the order a request meets them:
 *
 * 1. No request leaves the browser. L142 reads `store` before any import defines it, so the
 *    call rejects before transport. The `createApiClient` block above records that failure
 *    and the second one waiting behind it.
 * 2. No bearer credential exists. With L142 repaired, no committed line writes a token where
 *    L142 reads one, so `token` holds `undefined`, the test at L143 fails and L144 sets no
 *    `Authorization` header.
 * 3. The path selects the get-one route rather than the list route.
 *    `backend/app/main.py:L125-L128` mounts every router without a prefix, so the committed
 *    document routes are `/` and `/{document_id}`. The path `/documents` is one segment, so
 *    it matches `GET /{document_id}` at `backend/app/api/documents.py:L148` with `document_id`
 *    bound to the literal string `documents`. `GET /` at
 *    `backend/app/api/documents.py:L114`, the only route that returns a list, is never
 *    selected.
 * 4. The selected route rejects the request. `backend/app/api/documents.py:L149` injects
 *    `get_current_user`, which depends on the `OAuth2PasswordBearer` instance at
 *    `backend/app/api/auth.py:L88`. A request carrying no `Authorization` header answers
 *    HTTP 401 before the handler body runs.
 * 5. The handler fails its service call. A request carrying a valid token reaches
 *    `backend/app/api/documents.py:L186`, which passes one argument where
 *    `backend/app/services/document_service.py:L125` declares `document_id` and `user_id`, so
 *    Python raises `TypeError` and FastAPI answers HTTP 500.
 *
 * No layer produces a list, so this call buffers nothing. The route the path selects returns
 * one document, and the list route it bypasses is the only producer of the declared
 * `Document[]`. Intended behavior per documentation/Technical Specifications.md, SYSTEM
 * DESIGN > API DESIGN (L417): `GET /documents` returns the caller's documents. A repaired
 * path would buffer every document, content included, because
 * `backend/app/api/documents.py:L114-L146` declares no pagination, no page size and no field
 * projection, so the response would grow with the collection.
 * @example
 * const documents = await getDocuments();
 * // Cannot run today: `axios` is absent from frontend/package.json, and the interceptor raises.
 */
export const getDocuments = async (): Promise<Document[]> => {
  const response = await api.get<Document[]>('/documents');
  return response.data;
};

/**
 * Create one document through `POST /documents`.
 *
 * @param documentData - The new document payload, typed as `DocumentCreate`.
 * @returns A promise resolving to the Axios `response.data`, typed as `Document`.
 * @remarks The shared `api` instance applies the same request interceptor, so the call fails
 * at L142 exactly as `getDocuments` does.
 *
 * The `DocumentCreate` parameter type and the `Document` return type are compile-time
 * annotations. L247 returns `response.data` with no Zod parse and no date conversion, exactly
 * as recorded on `getDocuments`.
 *
 * The dispatch outcome differs from `getDocuments`. No `POST /{document_id}` route exists,
 * because `backend/app/api/documents.py:L148`, `:L30` and `:L39` register that path template
 * for GET, PUT and DELETE only. Starlette matches the one-segment path `/documents` against
 * that template, finds no handler for the method, and answers 405 Method Not Allowed. The
 * request never reaches `POST /` at `backend/app/api/documents.py:L56`.
 *
 * @example
 * const created = await createDocument(documentData);
 * // Cannot run today: L142 raises first, and `DocumentCreate` has no definition to shape the
 * // argument.
 */
export const createDocument = async (documentData: DocumentCreate): Promise<Document> => {
  const response = await api.post<Document>('/documents', documentData);
  return response.data;
};

/**
 * Replace one document through `PUT /documents/{documentId}`.
 *
 * @param documentId - Identifier interpolated into the request path.
 * @param documentData - The update payload, declared `DocumentUpdate`. That name is one of the
 * three unresolved imports at L80, so no client-side type states which fields the payload may
 * carry. L288 sends the value as the request body without inspecting it.
 * @returns A promise resolving to the Axios `response.data`, typed as `Document`.
 * @remarks The request replaces no field the caller leaves out. The server contract for this
 * operation is a partial patch: `backend/app/schema/document.py:L84-L96` declares only `title` and
 * `content` on `DocumentUpdate`, and `backend/app/services/document_service.py:L247` calls
 * `dict(exclude_unset=True)`, so only the fields a caller sets explicitly reach storage.
 *
 * The shared `api` instance applies the same request interceptor, so the call fails
 * at L142 exactly as `getDocuments` does. L289 returns `response.data` with no Zod parse and no
 * date conversion, exactly as recorded on `getDocuments`.
 *
 * L288 interpolates `documentId` into the path with no validation and no `encodeURIComponent`.
 * A caller-supplied value can therefore change the shape of the request Uniform Resource
 * Locator rather than only its last segment. A value carrying `/` adds a path segment and
 * retargets the request. A value carrying `?` starts a query string and truncates the path. A
 * value carrying `#` starts a fragment the browser never transmits. Nothing rejects the empty
 * string either, which sends `PUT /documents/` instead.
 *
 * The dispatch outcome differs again. `/documents/${documentId}` is two segments, and every
 * route the application registers is either the root or a single segment.
 * `backend/app/api/documents.py` registers `/` and `/{document_id}`,
 * `backend/app/api/users.py:L32` and `:L12` register `/me`, `backend/app/api/auth.py:L170` and
 * `:L42` register `/token` and `/register`, and `backend/app/api/templates.py` repeats the
 * document templates. No registered template matches two segments, so the response is 404
 * rather than the 405 that `createDocument` receives.
 *
 * @example
 * const updated = await updateDocument('doc-123', documentData);
 * // Cannot run today: L142 raises first, and `DocumentUpdate` has no definition to shape the
 * // second argument.
 */
export const updateDocument = async (documentId: string, documentData: DocumentUpdate): Promise<Document> => {
  const response = await api.put<Document>(`/documents/${documentId}`, documentData);
  return response.data;
};