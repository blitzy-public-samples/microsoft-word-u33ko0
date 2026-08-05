/** Centralize the document REST calls behind a module-private Axios instance.
 *
 * REST abbreviates Representational State Transfer. The three exported functions send every
 * request through one shared instance, which supplies the base URL and both interceptors.
 *
 * Line numbers below refer to the committed file, before this header existed.
 *
 * `axios` at L1 is absent from `frontend/package.json`, whose `dependencies` block spans
 * L6-L14 and names seven packages, so the import raises one TS2307 error.
 *
 * L3 imports `Document`, `DocumentCreate` and `DocumentUpdate` from `../schema/document`. The
 * path resolves and all three names are absent, because that module exports only the schema
 * values `DocumentSchema` and `DocumentVersionSchema` and declares no `z.infer` alias. Three
 * TS2305 errors follow. L2 imports `RootState` from `../store`, and
 * `frontend/src/store/index.ts:L12` does export it.
 *
 * L16 carries two independent faults. No import brings `store` into this module, and
 * `frontend/src/store/index.ts:L6-L9` registers only the `document` and `user` reducer keys,
 * so the `auth` key L16 reads does not exist. Supplying the missing import leaves the second
 * fault in place.
 *
 * L5 reads `REACT_APP_API_BASE_URL`, while `infrastructure/docker/docker-compose.yml:L11`
 * injects `REACT_APP_API_URL`. The two names differ, so the base URL resolves to `undefined`.
 * L5 holds the only `process.env` read in the frontend.
 *
 * Three symbols other modules import from here never appear in this file: `getDocument`
 * (`frontend/src/pages/Editor.tsx:L6`), `getTemplates`
 * (`frontend/src/pages/Templates.tsx:L4`) and `updateUserSettings`
 * (`frontend/src/pages/Settings.tsx:L4`).
 */

import axios, { AxiosInstance } from 'axios';
import { RootState } from '../store';
import { Document, DocumentCreate, DocumentUpdate } from '../schema/document';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

/**
 * Build the shared Axios instance, wiring its base URL, its default content type and both
 * interceptors.
 *
 * @returns The configured `AxiosInstance`.
 *
 * @remarks `createApiClient` carries no `export` keyword, so the symbol stays private to this
 * module. L12 mutates `instance.defaults.headers.common['Content-Type']` to
 * `application/json`, which then applies to every request the instance sends.
 *
 * The request interceptor at L14-L23 reads a token and, when one is present, sets the
 * `Authorization` header to `Bearer <token>`. L16 raises a `ReferenceError` before the
 * interceptor reaches that header, for the two reasons the file header records.
 *
 * The response interceptor at L25-L31 passes both outcomes straight through: L26 returns the
 * response unchanged and L29 re-rejects the error unchanged. L28 carries the file's only
 * pre-existing comment, inside that error branch.
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

/**
 * The module-private Axios instance, built once at module evaluation and shared by the three
 * exported functions.
 */
const api = createApiClient();

/**
 * Request the full document list through `GET /documents`.
 *
 * @returns A promise resolving to the Axios `response.data`, typed as `Document[]`.
 * @remarks Every call travels through the shared `api` instance, so the request interceptor
 * runs first and fails at L16. Neither interceptor handles a rejection, so errors reach the
 * caller unchanged. The path does not match the server either.
 * `backend/app/main.py:L49-L52` mounts the documents router without a prefix, so the
 * committed routes are `/` and `/{document_id}`, not `/documents` and
 * `/documents/{document_id}`.
 *
 * @example
 * const documents = await getDocuments();
 * // Cannot run today: `axios` is absent from frontend/package.json, and L16 raises first.
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
 * at L16 exactly as `getDocuments` does. The path mismatch recorded on `getDocuments` covers
 * this route as well.
 *
 * @example
 * const created = await createDocument(documentData);
 * // Cannot run today: L16 raises first, and `DocumentCreate` has no definition to shape the
 * // argument.
 */
export const createDocument = async (documentData: DocumentCreate): Promise<Document> => {
  const response = await api.post<Document>('/documents', documentData);
  return response.data;
};

/**
 * Update one document through `PUT /documents/${documentId}`.
 *
 * @param documentId - Identifier interpolated into the request path.
 * @param documentData - The replacement payload, typed as `DocumentUpdate`.
 * @returns A promise resolving to the Axios `response.data`, typed as `Document`.
 * @remarks The shared `api` instance applies the same request interceptor, so the call fails
 * at L16 exactly as `getDocuments` does. The server exposes `/{document_id}` for this
 * operation, per the path mismatch recorded on `getDocuments`.
 *
 * @example
 * const updated = await updateDocument('doc-123', documentData);
 * // Cannot run today: L16 raises first, and `DocumentUpdate` has no definition to shape the
 * // second argument.
 */
export const updateDocument = async (documentId: string, documentData: DocumentUpdate): Promise<Document> => {
  const response = await api.put<Document>(`/documents/${documentId}`, documentData);
  return response.data;
};