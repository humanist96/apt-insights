'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/lib/api-client';

interface User {
  id: number;
  email: string;
  name?: string;
  subscription_tier: string;
  subscription_expires_at?: string;
  created_at: string;
  last_login_at?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, confirmPassword: string, name?: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const saveTokens = useCallback((accessToken: string, refreshToken: string) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);

    // Set Authorization header for all future requests
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
  }, []);

  const clearTokens = useCallback(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete apiClient.defaults.headers.common['Authorization'];
  }, []);

  const refreshAccessToken = useCallback(async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      return false;
    }

    try {
      const response = await apiClient.post('/api/v1/auth/refresh', {
        refresh_token: refreshToken,
      });

      const { access_token, refresh_token: newRefreshToken } = response.data;
      saveTokens(access_token, newRefreshToken);

      return true;
    } catch (error) {
      clearTokens();
      return false;
    }
  }, [saveTokens, clearTokens]);

  const refreshUser = useCallback(async () => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    try {
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
      const response = await apiClient.get('/api/v1/auth/me');
      setUser(response.data);
    } catch (error) {
      // Try to refresh token
      const refreshed = await refreshAccessToken();
      if (refreshed) {
        // Retry getting user
        try {
          const response = await apiClient.get('/api/v1/auth/me');
          setUser(response.data);
        } catch {
          setUser(null);
          clearTokens();
        }
      } else {
        setUser(null);
        clearTokens();
      }
    } finally {
      setIsLoading(false);
    }
  }, [refreshAccessToken, clearTokens]);

  const login = useCallback(async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/api/v1/auth/login', {
        email,
        password,
      });

      const { access_token, refresh_token } = response.data;
      saveTokens(access_token, refresh_token);

      // Get user profile
      await refreshUser();
    } catch (error) {
      if (error instanceof Error) {
        throw new Error('Invalid email or password');
      }
      throw error;
    }
  }, [saveTokens, refreshUser]);

  const register = useCallback(async (
    email: string,
    password: string,
    confirmPassword: string,
    name?: string
  ) => {
    try {
      const response = await apiClient.post('/api/v1/auth/register', {
        email,
        password,
        confirm_password: confirmPassword,
        name,
      });

      const { access_token, refresh_token } = response.data;
      saveTokens(access_token, refresh_token);

      // Get user profile
      await refreshUser();
    } catch (error: unknown) {
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as { response?: { data?: { detail?: string } } };
        const message = axiosError.response?.data?.detail || 'Registration failed';
        throw new Error(message);
      }
      throw new Error('Registration failed');
    }
  }, [saveTokens, refreshUser]);

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);

    // Optional: Call logout endpoint
    apiClient.post('/api/v1/auth/logout').catch(() => {
      // Ignore errors
    });
  }, [clearTokens]);

  // Setup token refresh interceptor
  useEffect(() => {
    const interceptor = apiClient.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          const refreshed = await refreshAccessToken();
          if (refreshed) {
            return apiClient(originalRequest);
          }
        }

        return Promise.reject(error);
      }
    );

    return () => {
      apiClient.interceptors.response.eject(interceptor);
    };
  }, [refreshAccessToken]);

  // Auto-refresh token every 20 hours
  useEffect(() => {
    const interval = setInterval(() => {
      if (user) {
        refreshAccessToken();
      }
    }, 20 * 60 * 60 * 1000); // 20 hours

    return () => clearInterval(interval);
  }, [user, refreshAccessToken]);

  // Load user on mount
  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
