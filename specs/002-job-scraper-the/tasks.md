# Tasks: Job Scraper

**Input**: Design documents from `/specs/002-job-scraper-the/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `backend/`, `frontend/`

## Phase 3.1: Setup
- [X] T001 [P] Set up scraping libraries (e.g., BeautifulSoup, Scrapy) in `backend/requirements.txt`.
- [X] T002 [P] Configure SAST and DAST scanning tools in the CI/CD pipeline.

## Phase 3.2: Backend
- [X] T003 [P] Create `Job` model in `backend/src/models/job.py` based on `data-model.md`.
- [X] T004 [P] Create `Keyword` model in `backend/src/models/keyword.py` based on `data-model.md`.
- [X] T005 [P] Create a service for scraping jobs from LinkedIn in `backend/src/services/scraper_linkedin.py`.
- [X] T006 [P] Create a service for scraping jobs from Indeed in `backend/src/services/scraper_indeed.py`.
- [X] T007 [P] Create a service for scraping jobs from Dice in `backend/src/services/scraper_dice.py`.
- [X] T008 Create a main scraping service in `backend/src/services/scraper.py` that calls the individual scrapers.
- [X] T009 Implement keyword filtering logic in `backend/src/services/scraper.py`.
- [X] T010 Implement duplicate handling logic in `backend/src/services/scraper.py`.
- [X] T011 Create a service for managing jobs (save, apply, hide) in `backend/src/services/job_service.py`.
- [X] T012 Create API endpoints for managing jobs in `backend/src/api/jobs.py` based on `contracts/jobs.yml`.
- [X] T013 [P] Write contract tests for the job management endpoints in `backend/tests/contract/test_jobs.py`.
- [X] T014 [P] Write unit tests for the scraping services in `backend/tests/unit/test_scraping.py`.
- [X] T015 [P] Write unit tests for the job management service in `backend/tests/unit/test_job_service.py`.
- [X] T016 [P] Implement structured logging for the backend services.
- [X] T017 [P] Implement metrics for monitoring the backend services.

## Phase 3.3: Frontend
- [X] T018 [P] Create a new component for the job dashboard in `frontend/src/components/Dashboard.js`.
- [X] T019 [P] Create a service for fetching jobs from the backend in `frontend/src/services/jobService.js`.
- [X] T020 [P] Implement the job dashboard UI to display the list of jobs.
- [X] T021 [P] Implement the functionality to save, apply, and hide jobs on the dashboard.
- [X] T022 [P] Write unit tests for the Dashboard component in `frontend/src/tests/Dashboard.test.js`.
- [X] T023 [P] Write integration tests for the job management flow in `frontend/src/tests/integration/jobManagement.test.js`.

## Phase 3.4: Polish
- [ ] T024 Perform load testing on the dashboard to ensure it meets the response time target.
- [ ] T025 Perform security review of the new feature.
- [ ] T026 Update the main `README.md` with information about the new feature.

## Phase 3.5: End-to-end Testing
- [ ] T027 Write and execute end-to-end tests for the job scraping and management flow.

## Dependencies
- T003, T004 must be done before T011.
- T005, T006, T007 must be done before T008.
- T008 must be done before T009, T010.
- T011 must be done before T012.
- T013 must be done before T012.
- T014 must be done before T008.
- T015 must be done before T011.
- T019 must be done before T020.

## Parallel Example
```
# Launch T005-T007 together:
Task: "Create a service for scraping jobs from LinkedIn in backend/src/services/scraper_linkedin.py"
Task: "Create a service for scraping jobs from Indeed in backend/src/services/scraper_indeed.py"
Task: "Create a service for scraping jobs from Dice in backend/src/services/scraper_dice.py"
```
