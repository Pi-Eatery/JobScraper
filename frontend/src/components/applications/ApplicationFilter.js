import React, { useState } from 'react';

function ApplicationFilter({ onFilterChange }) {
  const [statusFilter, setStatusFilter] = useState('');
  const [companyFilter, setCompanyFilter] = useState('');
  const [jobTitleFilter, setJobTitleFilter] = useState('');

  const handleFilter = () => {
    onFilterChange({
      status: statusFilter,
      company: companyFilter,
      job_title: jobTitleFilter,
    });
  };

  return (
    <div
      style={{
        marginBottom: '20px',
        padding: '10px',
        border: '1px solid #ccc',
      }}
    >
      <h3>Filter Applications</h3>
      <div>
        <label htmlFor="statusFilter">Status:</label>
        <input
          type="text"
          id="statusFilter"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="companyFilter">Company:</label>
        <input
          type="text"
          id="companyFilter"
          value={companyFilter}
          onChange={(e) => setCompanyFilter(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="jobTitleFilter">Job Title:</label>
        <input
          type="text"
          id="jobTitleFilter"
          value={jobTitleFilter}
          onChange={(e) => setJobTitleFilter(e.target.value)}
        />
      </div>
      <button onClick={handleFilter}>Apply Filters</button>
    </div>
  );
}

export default ApplicationFilter;
