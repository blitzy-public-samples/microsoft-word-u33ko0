import axios, { AxiosInstance } from 'axios';
import { RootState } from '../store';
import { Document, DocumentCreate, DocumentUpdate } from '../schema/document';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

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

export const getDocuments = async (): Promise<Document[]> => {
  const response = await api.get<Document[]>('/documents');
  return response.data;
};

export const createDocument = async (documentData: DocumentCreate): Promise<Document> => {
  const response = await api.post<Document>('/documents', documentData);
  return response.data;
};

export const updateDocument = async (documentId: string, documentData: DocumentUpdate): Promise<Document> => {
  const response = await api.put<Document>(`/documents/${documentId}`, documentData);
  return response.data;
};