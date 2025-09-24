import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Dashboard from '../../components/Dashboard';
import * as jobService from '../../services/jobService';

// Mock the jobService module for integration tests
jest.mock('../../services/jobService');

describe('Job Management Integration Flow', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock initial fetchJobs call
    jobService.fetchJobs.mockResolvedValue([
      { id: 1, title: 'Software Engineer', company: 'Tech Corp', description: 'Develop software', application_link: 'http://techcorp.com/se', status: 'new' },
    ]);
  });

  test('user can save a job and see its status update', async () => {
    render(<Dashboard />);

    // Wait for the job to be displayed
    await waitFor(() => expect(screen.getByText(/Software Engineer/i)).toBeInTheDocument());
    expect(screen.getByText(/Status: new/i)).toBeInTheDocument();

    // Mock the saveJob call
    jobService.saveJob.mockResolvedValueOnce(
      { id: 1, title: 'Software Engineer', company: 'Tech Corp', description: 'Develop software', application_link: 'http://techcorp.com/se', status: 'saved' }
    );

    // Click the Save button
    const saveButton = screen.getByRole('button', { name: /Save/i });
    userEvent.click(saveButton);

    // Verify saveJob was called and status updated
    await waitFor(() => expect(jobService.saveJob).toHaveBeenCalledWith(1));
    expect(screen.getByText(/Status: saved/i)).toBeInTheDocument();
    expect(saveButton).toBeDisabled();
  });

  test('user can apply to a job and see its status update', async () => {
    render(<Dashboard />);

    await waitFor(() => expect(screen.getByText(/Software Engineer/i)).toBeInTheDocument());
    expect(screen.getByText(/Status: new/i)).toBeInTheDocument();

    jobService.applyJob.mockResolvedValueOnce(
      { id: 1, title: 'Software Engineer', company: 'Tech Corp', description: 'Develop software', application_link: 'http://techcorp.com/se', status: 'applied' }
    );

    const applyButton = screen.getByRole('button', { name: /Apply/i });
    userEvent.click(applyButton);

    await waitFor(() => expect(jobService.applyJob).toHaveBeenCalledWith(1));
    expect(screen.getByText(/Status: applied/i)).toBeInTheDocument();
    expect(applyButton).toBeDisabled();
  });

  test('user can hide a job and see its status update', async () => {
    render(<Dashboard />);

    await waitFor(() => expect(screen.getByText(/Software Engineer/i)).toBeInTheDocument());
    expect(screen.getByText(/Status: new/i)).toBeInTheDocument();

    jobService.hideJob.mockResolvedValueOnce(
      { id: 1, title: 'Software Engineer', company: 'Tech Corp', description: 'Develop software', application_link: 'http://techcorp.com/se', status: 'hidden' }
    );

    const hideButton = screen.getByRole('button', { name: /Hide/i });
    userEvent.click(hideButton);

    await waitFor(() => expect(jobService.hideJob).toHaveBeenCalledWith(1));
    expect(screen.getByText(/Status: hidden/i)).toBeInTheDocument();
    expect(hideButton).toBeDisabled();
  });
});
