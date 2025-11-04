import api from './api';

export const projectService = {
  getProjects: async (params) => {
    const response = await api.get('/api/project/', { params });
    return response.data;
  },

  getProject: async (id) => {
    const response = await api.get(`/api/project/${id}`);
    return response.data;
  },

  createProject: async (data) => {
    const response = await api.post('/api/project/', data);
    return response.data;
  },

  updateProject: async (id, data) => {
    const response = await api.patch(`/api/project/${id}`, data);
    return response.data;
  },

  deleteProject: async (id) => {
    const response = await api.delete(`/api/project/${id}`);
    return response.data;
  },
};

