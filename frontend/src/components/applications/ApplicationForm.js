import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';

function ApplicationForm({ application, onSave, onCancel }) {
    const { token } = useAuth();
    const [formData, setFormData] = useState({
        job_title: '',
        company: '',
        application_date: '',
        status: 'Applied',
        job_board: '',
        url: '',
        notes: '',
        keywords: ''
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
                keywords: application.keywords || ''
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
                keywords: ''
            });
        }
    }, [application]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError('');

        const apiUrl = application
            ? `http://localhost:8000/api/applications/${application.id}`
            : 'http://localhost:8000/api/applications/';
        const method = application ? 'PUT' : 'POST';

        try {
            const response = await fetch(apiUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to save application');
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
                <button type="button" onClick={onCancel}>Cancel</button>
            </form>
        </div>
    );
}

export default ApplicationForm;