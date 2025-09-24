import React, { createContext, useState, useContext, useEffect } from 'react';
import { api } from 'services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('access_token'));

    useEffect(() => {
        if (token) {
            // In a real app, you'd decode the token or fetch user data
            // to set the `user` state. For now, a placeholder.
            setUser({ username: 'testuser' });
        } else {
            setUser(null);
        }
    }, [token]);

    const login = async (username, password) => {
        try {
            const data = await api.login(username, password);
            localStorage.setItem('access_token', data.access_token);
            setToken(data.access_token);
            setUser({ username: username }); // Set user info, possibly fetched from API
            return true;
        } catch (error) {
            console.error("Login error:", error);
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        setToken(null);
        setUser(null);
    };

    const isAuthenticated = () => {
        return !!token;
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};