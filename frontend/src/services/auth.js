import api from './api';

export const login = async (usernameOrEmail, password) => {
  try {
    const response = await api.post('token/', { username: usernameOrEmail, password });
    const data = response.data;
    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);
    return data;
  } catch (err) {
    const response = await api.post('users/token/email/', { email: usernameOrEmail, password });
    const data = response.data;
    localStorage.setItem('access', data.access);
    if (data.refresh) localStorage.setItem('refresh', data.refresh);
    return data;
  }
};

export const register = async (userData) => {
  const response = await api.post('users/users/', userData);
  return response.data;
};
