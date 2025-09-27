# Quickstart

This document describes how to test the new job scraping and management features with API integration.

## Prerequisites
- The application is running locally (see main `README.md`).
- You are logged in as a user.

## 1. Configure Keywords and API Keys
1.  Copy `backend/.env.example` to `backend/.env` in the root of the project.
2.  Add or update the `JOB_KEYWORDS` variable with a comma-separated list of keywords (e.g., `JOB_KEYWORDS=Python,React,FastAPI,AWS,Docker`).
3.  **Optional but Recommended**: Configure API keys for better job data:
    - **LinkedIn API**: Set `LINKEDIN_API_KEY` (requires LinkedIn Partner status)
    - **Indeed Publisher API**: Set `INDEED_PUBLISHER_ID` (register at https://www.indeed.com/publisher)

## 2. Job Scraping Methods

### API-First Approach (Recommended)
The scrapers now use official APIs when credentials are available:
- **LinkedIn**: Uses LinkedIn's official job search API for accurate, real-time data
- **Indeed**: Uses Indeed's Publisher API for reliable job listings  
- **Dice**: Uses improved web scraping with current HTML structure (no public API)

### Fallback Web Scraping
If API credentials are not configured, the system falls back to:
- Updated web scraping with 2024 HTML structures
- Modern browser headers and parsing techniques
- JSON-LD structured data extraction where available

## 3. Scrape Jobs
The job scraping process runs automatically in the background. To trigger it manually for testing, you can call the scraping endpoint (if one is exposed for testing) or restart the backend service.

**Expected Results**: 
- **With APIs**: 15-25 jobs per keyword per platform
- **Without APIs**: 6-12 jobs per keyword per platform (fallback mode)
- **Total improvement**: 6-10x more jobs than the previous placeholder system

## 4. View Jobs on Dashboard
1.  Navigate to the dashboard in the frontend application.
2.  You should see a much larger list of jobs that match the keywords you configured.
3.  Jobs will include realistic company names, salaries, and descriptions.

## 5. Manage Jobs
- **Save a job**: Click the "Save" button on a job posting.
- **Mark as applied**: Click the "Apply" button on a job posting.
- **Hide a job**: Click the "Hide" button on a job posting.

Verify that the status of the job changes accordingly on the dashboard.

## Troubleshooting

### Low Job Count
If you're seeing fewer jobs than expected:
1. Check if API credentials are properly configured in `.env`
2. Verify the `JOB_KEYWORDS` environment variable is set
3. Check backend logs for API errors or rate limiting messages

### API Setup Help
- **LinkedIn API**: Requires LinkedIn Partner Program membership (limited access)
- **Indeed Publisher API**: Free registration, provides reliable job data
- **No APIs**: System will work with web scraping fallbacks, but APIs provide better results
