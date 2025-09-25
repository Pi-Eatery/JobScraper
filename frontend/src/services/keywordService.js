const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const fetchKeywords = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/keywords/`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching keywords:", error);
    throw error;
  }
};

export const addKeyword = async (term) => {
  try {
    const response = await fetch(`${API_BASE_URL}/keywords/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ term }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error adding keyword:", error);
    throw error;
  }
};

export const deleteKeyword = async (keywordId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/keywords/${keywordId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return true; // Or handle response if backend sends confirmation
  } catch (error) {
    console.error("Error deleting keyword:", error);
    throw error;
  }
};
