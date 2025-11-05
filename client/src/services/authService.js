import api from './api';

export const authService = {
  register: async (data) => {
    const response = await api.post('/api/auth/register', data);
    return response.data;
  },

  login: async (credentials) => {
    const response = await api.post('/api/auth/login', credentials);
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },

  getAllUsers: async () => {
    const response = await api.get('/api/auth/users');
    return response.data;
  },

  logout: () => {
    return Promise.resolve();
  },
};

