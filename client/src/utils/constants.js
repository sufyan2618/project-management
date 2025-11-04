export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const TASK_STATUS = {
  TODO: 'todo',
  IN_PROGRESS: 'in-progress',
  DONE: 'done',
};

export const USER_ROLES = {
  ADMIN: 'admin',
  USER: 'user',
};

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  USER: 'user',
};

export const QUERY_KEYS = {
  PROJECTS: 'projects',
  PROJECT_DETAIL: 'project-detail',
  TASKS: 'tasks',
  TASK_DETAIL: 'task-detail',
  USER_PROFILE: 'user-profile',
};

