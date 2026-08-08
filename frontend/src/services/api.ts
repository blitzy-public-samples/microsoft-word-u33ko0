/**
 * Build the axios client for the document API and expose three document calls.
 *
 * The base URL comes from `REACT_APP_API_BASE_URL`, and the Compose file injects
 * `REACT_APP_API_URL`, so the two names do not meet and the client resolves an
 * undefined base URL. Requests then go to the origin that served the page.
 *
 * Three types are imported from `../schema/document`, which exports none of them.
 * `store` is read inside the request interceptor and never imported. Three pages
 * import `getDocument`, `getTemplates` and `updateUserSettings` from here, and this
 * module declares none of the three.
 *
 * `axios` is imported and `frontend/package.json` does not declare it.
 *
 * @see ./README.md
 */
import axios, { AxiosInstance } from 'axios';
import { RootState } from '../store';
import { Document, DocumentCreate, DocumentUpdate } from '../schema/document';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

/**
 * Create the shared axios instance with a JSON content type and two interceptors.
 *
 * @returns The configured instance. The request interceptor reads
 * `state.auth.token`, and the store registers no `auth` slice, so the read raises
 * even once `store` is imported. The response interceptor passes both outcomes
 * through unchanged, so it adds nothing today.
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

/** The shared client every call below uses, created once at module load. */
const api = createApiClient();

/**
 * Fetch every document the caller can see.
 *
 * @returns A promise for the document array. `/documents` is one segment, matching the protected
 * `GET /{document_id}`. No intended route is reached: 401 without a token, 500 once authenticated.
 */
export const getDocuments = async (): Promise<Document[]> => {
  const response = await api.get<Document[]>('/documents');
  return response.data;
};

/**
 * Create a document.
 *
 * @param documentData - Title, content and optional owner for the new document.
 * @returns A promise for the created document. No route declares `POST` on a single segment, so
 * Starlette answers 405 before any dependency runs.
 */
export const createDocument = async (documentData: DocumentCreate): Promise<Document> => {
  const response = await api.post<Document>('/documents', documentData);
  return response.data;
};

/**
 * Apply a partial update to one document.
 *
 * @param documentId - Identifier of the document to change.
 * @param documentData - The fields to change.
 * @returns A promise for the updated document. The two-segment path `/documents/{id}` matches no
 * declared route, so Starlette answers 404 before any dependency runs.
 */
export const updateDocument = async (documentId: string, documentData: DocumentUpdate): Promise<Document> => {
  const response = await api.put<Document>(`/documents/${documentId}`, documentData);
  return response.data;
};