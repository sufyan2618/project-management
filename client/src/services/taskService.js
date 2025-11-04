import api from './api';

export const taskService = {
  getTasks: async (params) => {
    const response = await api.get('/api/task/', { params });
    return response.data;
  },

  getTask: async (id) => {
    const response = await api.get(`/api/task/${id}`);
    return response.data;
  },

  createTask: async (data) => {
    const response = await api.post('/api/task/', data);
    return response.data;
  },

  updateTask: async (id, data) => {
    const response = await api.patch(`/api/task/${id}`, data);
    return response.data;
  },

  deleteTask: async (id) => {
    const response = await api.delete(`/api/task/${id}`);
    return response.data;
  },
};

