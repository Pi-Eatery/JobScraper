import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Dashboard from '../components/Dashboard';
import * as jobService from '../services/jobService';

// Mock the jobService module
jest.mock('../services/jobService');

describe('Dashboard', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
  });

  test('renders loading state initially', () => {
    jobService.fetchJobs.mockReturnValueOnce(new Promise(() => {})); // Never resolve to keep it in loading state
    render(<Dashboard />);
    expect(screen.getByText(/Loading jobs.../i)).toBeInTheDocument();
  });

  test('renders error message if fetching jobs fails', async () => {
    const errorMessage = 'Failed to fetch jobs';
    jobService.fetchJobs.mockRejectedValueOnce(new Error(errorMessage));
    render(<Dashboard />);
    await waitFor(() => expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument());
  });

  test('renders no jobs message if no jobs are returned', async () => {
    jobService.fetchJobs.mockResolvedValueOnce([]);
    render(<Dashboard />);
    await waitFor(() => expect(screen.getByText(/No jobs found/i)).toBeInTheDocument());
  });

  test('renders a list of jobs', async () => {
    const mockJobs = [
      { id: 1, title: 'Job 1', company: 'Company A', description: 'Desc 1', application_link: 'link1', status: 'new' },
      { id: 2, title: 'Job 2', company: 'Company B', description: 'Desc 2', application_link: 'link2', status: 'saved' },
    ];
    jobService.fetchJobs.mockResolvedValueOnce(mockJobs);
    render(<Dashboard />);

    await waitFor(() => expect(screen.getByText(/Job 1/i)).toBeInTheDocument());
    expect(screen.getByText(/Company A/i)).toBeInTheDocument();
    expect(screen.getByText(/Job 2/i)).toBeInTheDocument();
    expect(screen.getByText(/Company B/i)).toBeInTheDocument();
  });

  test('calls saveJob when Save button is clicked', async () => {
    const mockJobs = [
      { id: 1, title: 'Job 1', company: 'Company A', description: 'Desc 1', application_link: 'link1', status: 'new' },
    ];
    jobService.fetchJobs.mockResolvedValueOnce(mockJobs);
    jobService.saveJob.mockResolvedValueOnce({ ...mockJobs[0], status: 'saved' });

    render(<Dashboard />);
    await waitFor(() => expect(screen.getByText(/Job 1/i)).toBeInTheDocument());

    const saveButton = screen.getByRole('button', { name: /Save/i });
    userEvent.click(saveButton);

    await waitFor(() => expect(jobService.saveJob).toHaveBeenCalledWith(1));
    await waitFor(() => expect(screen.getByText(/Status: saved/i)).toBeInTheDocument());
  });

  test('calls applyJob when Apply button is clicked', async () => {
    const mockJobs = [
      { id: 1, title: 'Job 1', company: 'Company A', description: 'Desc 1', application_link: 'link1', status: 'new' },
    ];
    jobService.fetchJobs.mockResolvedValueOnce(mockJobs);
    jobService.applyJob.mockResolvedValueOnce({ ...mockJobs[0], status: 'applied' });

    render(<Dashboard />);
    await waitFor(() => expect(screen.getByText(/Job 1/i)).toBeInTheDocument());

    const applyButton = screen.getByRole('button', { name: /Apply/i });
    userEvent.click(applyButton);

    await waitFor(() => expect(jobService.applyJob).toHaveBeenCalledWith(1));
    await waitFor(() => expect(screen.getByText(/Status: applied/i)).toBeInTheDocument());
  });

  test('calls hideJob when Hide button is clicked', async () => {
    const mockJobs = [
      { id: 1, title: 'Job 1', company: 'Company A', description: 'Desc 1', application_link: 'link1', status: 'new' },
    ];
    jobService.fetchJobs.mockResolvedValueOnce(mockJobs);
    jobService.hideJob.mockResolvedValueOnce({ ...mockJobs[0], status: 'hidden' });

    render(<Dashboard />);
    await waitFor(() => expect(screen.getByText(/Job 1/i)).toBeInTheDocument());

    const hideButton = screen.getByRole('button', { name: /Hide/i });
    userEvent.click(hideButton);

    await waitFor(() => expect(jobService.hideJob).toHaveBeenCalledWith(1));
    await waitFor(() => expect(screen.getByText(/Status: hidden/i)).toBeInTheDocument());
  });
});
