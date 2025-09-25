import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { api } from 'services/api';

function ApplicationForm({ application, onSave, onCancel }) {
  useAuth(); // Call useAuth to ensure context is loaded, but don't destructure token
  const [formData, setFormData] = useState({
    job_title: '',
    company: '',
    application_date: '',
    status: 'Applied',
    job_board: '',
    url: '',
    notes: '',
    keywords: '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    if (application) {
      setFormData({
        job_title: application.job_title || '',
        company: application.company || '',
        application_date: application.application_date || '',
        status: application.status || 'Applied',
        job_board: application.job_board || '',
        url: application.url || '',
        notes: application.notes || '',
        keywords: application.keywords || '',
      });
    } else {
      // Reset form for new application if no application prop is passed
      setFormData({
        job_title: '',
        company: '',
        application_date: '',
        status: 'Applied',
        job_board: '',
        url: '',
        notes: '',
        keywords: '',
      });
    }
  }, [application]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    try {
      if (application) {
        await api.updateApplication(application.id, formData);
      } else {
        await api.createApplication(formData);
      }
      onSave(); // Notify parent component that save was successful
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>{application ? 'Edit Application' : 'Add New Application'}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="job_title">Job Title:</label>
          <input
            type="text"
            id="job_title"
            name="job_title"
            value={formData.job_title}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="company">Company:</label>
          <input
            type="text"
            id="company"
            name="company"
            value={formData.company}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="application_date">Application Date:</label>
          <input
            type="date"
            id="application_date"
            name="application_date"
            value={formData.application_date}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="status">Status:</label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value="Applied">Applied</option>
            <option value="Interviewing">Interviewing</option>
            <option value="Rejected">Rejected</option>
            <option value="Offer">Offer</option>
            <option value="Accepted">Accepted</option>
          </select>
        </div>
        <div>
          <label htmlFor="job_board">Job Board:</label>
          <input
            type="text"
            id="job_board"
            name="job_board"
            value={formData.job_board}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="url">URL:</label>
          <input
            type="url"
            id="url"
            name="url"
            value={formData.url}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="notes">Notes:</label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="keywords">Keywords:</label>
          <input
            type="text"
            id="keywords"
            name="keywords"
            value={formData.keywords}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Save Application</button>
        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </form>
    </div>
  );
}

export default ApplicationForm;
