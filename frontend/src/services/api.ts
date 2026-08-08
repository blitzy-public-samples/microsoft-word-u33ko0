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

const api = createApiClient();

/**
 * Fetch every document the caller can see.
 *
 * @returns A promise for the document array. The module does not compile, and the request
 * interceptor reads an undefined `store`, so no request is issued. Any backend route match
 * for the one-segment `/documents` path is therefore conditional on repairing both faults.
 */
export const getDocuments = async (): Promise<Document[]> => {
  const response = await api.get<Document[]>('/documents');
  return response.data;
};

/**
 * Create a document.
 *
 * @param documentData - The unresolved `DocumentCreate` argument; its fields are not
 * declared in this frontend tree.
 * @returns A promise for the created document. The same two faults block the call, so no
 * status is observed; a `POST` on the one-segment path would match no declared route.
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
 * @returns A promise for the updated document. The same two faults block the call, so no
 * status is observed; the two-segment path would match no declared route either.
 */
export const updateDocument = async (documentId: string, documentData: DocumentUpdate): Promise<Document> => {
  const response = await api.put<Document>(`/documents/${documentId}`, documentData);
  return response.data;
};