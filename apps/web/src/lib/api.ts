// src/lib/api.ts
import axios from 'axios';

// Django API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/auth/phone';
      }
    }

    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  // Register user with phone
  register: (data: { phone: string; first_name: string; gender: string; birth_date?: string }) =>
    api.post('/auth/register/', data),

  // Send OTP to phone
  sendOTP: (phone: string) =>
    api.post('/auth/send-otp/', { phone }),

  // Verify OTP and login
  verifyOTP: (phone: string, otp_code: string) =>
    api.post('/auth/verify-otp/', { phone, otp_code }),

  // Get user profile
  getProfile: () =>
    api.get('/auth/profile/'),

  // Update user profile
  updateProfile: (data: any) =>
    api.patch('/auth/profile/update/', data),
};

export default api;