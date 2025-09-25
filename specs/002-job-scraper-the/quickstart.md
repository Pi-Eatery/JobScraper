# Quickstart

This document describes how to test the new job scraping and management features.

## Prerequisites
- The application is running locally (see main `README.md`).
- You are logged in as a user.

## 1. Configure Keywords
1.  Open the `.env` file in the root of the project.
2.  Add or update the `JOB_KEYWORDS` variable with a comma-separated list of keywords (e.g., `JOB_KEYWORDS=Python,React,FastAPI`).

## 2. Scrape Jobs
The job scraping process runs automatically in the background. To trigger it manually for testing, you can call the scraping endpoint (if one is exposed for testing) or restart the backend service.

## 3. View Jobs on Dashboard
1.  Navigate to the dashboard in the frontend application.
2.  You should see a list of jobs that match the keywords you configured.

## 4. Manage Jobs
- **Save a job**: Click the "Save" button on a job posting.
- **Mark as applied**: Click the "Apply" button on a job posting.
- **Hide a job**: Click the "Hide" button on a job posting.

Verify that the status of the job changes accordingly on the dashboard.
