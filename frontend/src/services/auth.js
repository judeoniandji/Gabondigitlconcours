import api from './api';

export const login = async (email, password) => {
  const response = await api.post('token/', { email, password });
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('users/', userData);
  return response.data;
};
