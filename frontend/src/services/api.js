import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const url = config.url || '';
  const AUTH_SKIP = ['token/', 'users/token/email/', 'users/users/'];
  if (!AUTH_SKIP.some((p) => url.endsWith(p))) {
    const token = localStorage.getItem('access');
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
