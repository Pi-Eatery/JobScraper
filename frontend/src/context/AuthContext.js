import React, { createContext, useState, useContext, useEffect } from 'react';
import { api } from 'services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => {
    const storedToken = localStorage.getItem('access_token');
    console.log('AuthContext - Initial token from localStorage:', storedToken);
    return storedToken;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('AuthContext - useEffect triggered. Current token:', token);
    if (token) {
      if (!user) {
        setUser({ username: 'placeholder' }); // Or fetch user details from API
      }
    } else {
      setUser(null);
    }
    setLoading(false);
  }, [token, user]);

  const login = async (username, password) => {
    try {
      setLoading(true);
      const data = await api.login(username, password);
      console.log('AuthContext - API login data:', data);
      console.log(
        'AuthContext - API login data.access_token:',
        data.access_token
      );
      localStorage.setItem('access_token', data.access_token);
      console.log(
        'AuthContext - Token set in localStorage:',
        localStorage.getItem('access_token')
      );
      setToken(data.access_token);
      setUser({ username: username });
      setLoading(false);
      return true;
    } catch (error) {
      console.error('Login error:', error);
      setLoading(false);
      throw error;
    }
  };

  const logout = () => {
    console.log('AuthContext - Logging out.');
    localStorage.removeItem('access_token');
    setToken(null);
    setUser(null);
    setLoading(false);
  };

  const isAuthenticated = () => {
    console.log('AuthContext - isAuthenticated check. Current token:', token);
    return !!token;
  };

  return (
    <AuthContext.Provider
      value={{ user, token, login, logout, isAuthenticated, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
