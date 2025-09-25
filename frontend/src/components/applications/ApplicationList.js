import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext'; // Assuming AuthContext provides the token
import { api } from 'services/api';

function ApplicationList() {
  const { token, isAuthenticated } = useAuth();
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated()) {
      setError('Please log in to view applications.');
      setLoading(false);
      return;
    }

    const fetchApplications = async () => {
      try {
        const data = await api.getApplications();
        setApplications(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, [token, isAuthenticated]);

  if (loading) {
    return <div>Loading applications...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Job Applications</h2>
      {applications.length === 0 ? (
        <p>No applications found. Start by adding one!</p>
      ) : (
        <ul>
          {applications.map((app) => (
            <li key={app.id}>
              <strong>{app.job_title}</strong> at {app.company} - {app.status}{' '}
              (Applied on: {app.application_date})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ApplicationList;
