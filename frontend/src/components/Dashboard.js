import React, { useState, useEffect } from 'react';
import { fetchJobs, saveJob, applyJob, hideJob } from '../services/jobService';

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getJobs = async () => {
    try {
      const fetchedJobs = await fetchJobs();
      setJobs(fetchedJobs);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getJobs();
  }, []);

  const handleAction = async (jobId, action) => {
    try {
      let updatedJob;
      if (action === 'save') {
        updatedJob = await saveJob(jobId);
      } else if (action === 'apply') {
        updatedJob = await applyJob(jobId);
      } else if (action === 'hide') {
        updatedJob = await hideJob(jobId);
      }
      setJobs(jobs.map((job) => (job.id === jobId ? updatedJob : job)));
    } catch (err) {
      console.error(`Error performing ${action} on job ${jobId}:`, err);
      setError(err);
    }
  };

  if (loading) {
    return <div>Loading jobs...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div className="dashboard-container">
      <h1>Job Dashboard</h1>
      {jobs.length === 0 ? (
        <p>
          No jobs found. Try adjusting your keywords or wait for new scrapes.
        </p>
      ) : (
        <div className="job-list">
          {jobs.map((job) => (
            <div key={job.id} className="job-card">
              <h2>{job.title}</h2>
              <h3>{job.company}</h3>
              <p>{job.description}</p>
              <a
                href={job.application_link}
                target="_blank"
                rel="noopener noreferrer"
              >
                Apply
              </a>
              {job.salary && <p>Salary: {job.salary}</p>}
              <p>Status: {job.status}</p>
              <div className="job-actions">
                <button
                  onClick={() => handleAction(job.id, 'save')}
                  disabled={job.status === 'saved'}
                >
                  Save
                </button>
                <button
                  onClick={() => handleAction(job.id, 'apply')}
                  disabled={job.status === 'applied'}
                >
                  Apply
                </button>
                <button
                  onClick={() => handleAction(job.id, 'hide')}
                  disabled={job.status === 'hidden'}
                >
                  Hide
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
