import axios from 'axios';
import { RootState } from '../store';
import { User } from '../schema/user';

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

export const logout = async (): Promise<void> => {
  try {
    await axios.post('/auth/logout');
    localStorage.removeItem('accessToken');
  } catch (error) {
    console.error('Logout failed', error);
  }
};

export const getCurrentUser = async (): Promise<User> => {
  try {
    const response = await axios.get('/auth/me');
    return response.data as User;
  } catch (error) {
    throw new Error('Failed to fetch current user');
  }
};