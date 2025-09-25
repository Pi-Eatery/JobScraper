const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
};

export const fetchJobs = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching jobs:", error);
    throw error;
  }
};

export const updateJobStatus = async (jobId, status) => {
  try {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/status`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ status }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error updating job ${jobId} status to ${status}:`, error);
    throw error;
  }
};

export const saveJob = async (jobId) => updateJobStatus(jobId, 'saved');
export const applyJob = async (jobId) => updateJobStatus(jobId, 'applied');
export const hideJob = async (jobId) => updateJobStatus(jobId, 'hidden');
