const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const handleResponse = async (response) => {
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Something went wrong');
    }
    return response.json();
};

const getToken = () => localStorage.getItem('access_token');

const authHeader = () => {
    const token = getToken();
    return token ? { 'Authorization': `Bearer ${token}` } : {};
};

export const api = {
    // Auth endpoints
    register: async (username, email, password) => {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password }),
        });
        return handleResponse(response);
    },

    login: async (username, password) => {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        return handleResponse(response);
    },

    // Job Application endpoints
    getApplications: async () => {
        const response = await fetch(`${API_BASE_URL}/applications/`, {
            method: 'GET',
            headers: { ...authHeader(), 'Content-Type': 'application/json' },
        });
        return handleResponse(response);
    },

    createApplication: async (applicationData) => {
        const response = await fetch(`${API_BASE_URL}/applications/`, {
            method: 'POST',
            headers: { ...authHeader(), 'Content-Type': 'application/json' },
            body: JSON.stringify(applicationData),
        });
        return handleResponse(response);
    },

    getApplication: async (id) => {
        const response = await fetch(`${API_BASE_URL}/applications/${id}`, {
            method: 'GET',
            headers: { ...authHeader(), 'Content-Type': 'application/json' },
        });
        return handleResponse(response);
    },

    updateApplication: async (id, applicationData) => {
        const response = await fetch(`${API_BASE_URL}/applications/${id}`, {
            method: 'PUT',
            headers: { ...authHeader(), 'Content-Type': 'application/json' },
            body: JSON.stringify(applicationData),
        });
        return handleResponse(response);
    },

    deleteApplication: async (id) => {
        const response = await fetch(`${API_BASE_URL}/applications/${id}`, {
            method: 'DELETE',
            headers: { ...authHeader(), 'Content-Type': 'application/json' },
        });
        return handleResponse(response);
    },
};