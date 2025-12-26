import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/';

export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

export default api;
