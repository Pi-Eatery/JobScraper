# Tasks: Job Scraper

**Input**: Design documents from `/specs/002-job-scraper-the/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `backend/`, `frontend/`

## Phase 3.1: Setup & Core Infrastructure

*   **T001 [P]**: Set up scraping libraries (e.g., BeautifulSoup, Scrapy) in `backend/pyproject.toml` and `poetry.lock`. (Related to FR-004)
*   **T002 [P]**: Configure SAST and DAST scanning tools in the CI/CD pipeline (`.github/workflows/backend_ci.yml`, `.github/workflows/frontend_ci.yml`). (Related to Constitution II. Automated Testing & Quality Gates - SHOULD)
*   **T003 [P]**: Implement TLS/SSL encryption for data in transit. (Addressing D1 Critical) (Related to Constitution I. Security by Design - MUST)
*   **T004 [P]**: Define and automate rollback procedures for deployments (`.github/workflows/backend_cd.yml`, `.github/workflows/frontend_cd.yml`). (Addressing D5 Critical) (Related to Constitution V. Continuous Delivery & Deployment - MUST)
*   **T005 [P]**: Configure Cloudflare Tunnel for frontend (`frontend/nginx.conf`) and backend access. (Infrastructure setup)

## Phase 3.2: Backend Models & Services (TDD - Tests First)

*   **T006 [P]**: Create `Job` model in `backend/src/models/job.py` based on `data-model.md`. (Related to Key Entities - Job)
*   **T007 [P]**: Create `Keyword` model in `backend/src/models/keyword.py` for user-managed keywords based on `data-model.md`. (Related to Key Entities - Keyword)
*   **T008 [P]**: Write unit tests for `Job` model in `backend/tests/unit/test_job_model.py`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)
*   **T009 [P]**: Write unit tests for `Keyword` model in `backend/tests/unit/test_keyword_model.py`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)
*   **T010 [P]**: Create a service for scraping jobs from LinkedIn in `backend/src/services/scraper_linkedin.py`. (Related to FR-004)
*   **T011 [P]**: Create a service for scraping jobs from Indeed in `backend/src/services/scraper_indeed.py`. (Related to FR-004)
*   **T012 [P]**: Create a service for scraping jobs from Dice in `backend/src/services/scraper_dice.py`. (Related to FR-004)
*   **T013**: Create a main scraping service in `backend/src/services/scraper.py` that calls the individual scrapers. (Related to FR-004)
*   **T014**: Implement keyword filtering logic in `backend/src/services/scraper.py` using database-managed keywords. (Related to FR-005)
*   **T015**: Implement duplicate handling logic in `backend/src/services/scraper.py`. (Related to FR-007)
*   **T016 [P]**: Write unit tests for the scraping services in `backend/tests/unit/test_scraping.py`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)
*   **T017**: Create a service for managing jobs (save, apply, hide) in `backend/src/services/job_service.py`. (Related to FR-008, FR-009, FR-010)
*   **T018 [P]**: Write unit tests for the job management service in `backend/tests/unit/test_job_service.py`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)

## Phase 3.3: Backend API & Security

*   **T019**: Create API endpoints for managing jobs in `backend/src/api/jobs.py` based on `contracts/jobs.yml`. (Related to FR-008, FR-009, FR-010)
*   **T020 [P]**: Write contract tests for the job management endpoints in `backend/tests/contract/test_jobs.py`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)
*   **T020a**: Create API endpoints for managing keywords in `backend/src/api/keywords.py`. (Related to Key Entities - Keyword)
*   **T020b [P]**: Write contract tests for the keyword management endpoints in `backend/tests/contract/test_keywords.py`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)
*   **T021**: Implement input validation and sanitization for all user-supplied data in API endpoints (`backend/src/api/`). (Addressing D2 Critical) (Related to Constitution I. Security by Design - MUST)
*   **T022**: Implement access control mechanisms for API endpoints (`backend/src/api/`). (Addressing D3 Critical) (Related to Constitution I. Security by Design - MUST)
*   **T023 [P]**: Implement structured logging for the backend services (`backend/src/`). (Related to NFR-002, Constitution IV. Observability & Monitoring - MUST)
*   **T024 [P]**: Implement metrics for monitoring the backend services (`backend/src/`). (Related to Constitution IV. Observability & Monitoring - MUST)

## Phase 3.4: Frontend

*   **T025 [P]**: Create a new component for the job dashboard in `frontend/src/components/Dashboard.js`. (Related to FR-003)
*   **T026 [P]**: Create a service for fetching jobs from the backend in `frontend/src/services/jobService.js`. (Related to FR-003, FR-006)
*   **T027 [P]**: Implement the job dashboard UI to display the list of jobs. (Related to FR-003, FR-006)
*   **T028 [P]**: Implement the functionality to save, apply, and hide jobs on the dashboard. (Related to FR-008, FR-009, FR-010)
*   **T028a [P]**: Create a UI component for managing user-defined keywords in `frontend/src/components/KeywordManager.js`. (Related to Key Entities - Keyword)
*   **T028b [P]**: Implement functionality to add, edit, and delete keywords in `frontend/src/services/keywordService.js` and `frontend/src/components/KeywordManager.js`. (Related to Key Entities - Keyword)
*   **T028c [P]**: Write unit tests for the KeywordManager component in `frontend/src/tests/KeywordManager.test.js`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)
*   **T029 [P]**: Write unit tests for the Dashboard component in `frontend/src/tests/Dashboard.test.js`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)
*   **T030 [P]**: Write integration tests for the job management flow in `frontend/src/tests/integration/jobManagement.test.js`. (Related to Constitution II. Automated Testing & Quality Gates - MUST)

## Phase 3.5: Polish & Testing

*   **T031**: Perform load testing on the dashboard to ensure it meets the response time target (NFR-003). (Related to NFR-003, Constitution II. Automated Testing & Quality Gates - SHOULD)
*   **T032**: Perform security review of the new feature. (Related to Constitution I. Security by Design - SHOULD)
*   **T033**: Update the main `README.md` with information about the new feature. (Documentation)
*   **T034**: Write and execute end-to-end tests for the job scraping and management flow. (Related to Constitution II. Automated Testing & Quality Gates - MUST)
*   **T035**: Document and enforce version control and review processes for infrastructure changes. (Addressing D4 High) (Related to Constitution III. Infrastructure as Code - MUST)
*   **T036**: Define and implement availability testing or monitoring specifically for NFR-004. (Addressing E2 Medium) (Related to NFR-004, Constitution IV. Observability & Monitoring - MUST)

## Dependencies

*   T006, T007 must be done before T017.
*   T008, T009 must be done before T017.
*   T010, T011, T012 must be done before T013.
*   T013 must be done before T014, T015.
*   T016 must be done before T013.
*   T017 must be done before T019.
*   T018 must be done before T019.
*   T019 must be done before T020, T020a, T021, T022.
*   T007 must be done before T020a.
*   T020a must be done before T020b, T028b.
*   T028a must be done before T028b.
*   T028b must be done before T028c.
*   T026 must be done before T027.
*   T027 must be done before T028.
*   T029 must be done before T027.
*   T030 must be done before T028.
*   T031, T032, T033, T034, T035, T036 can be done in parallel after core implementation.

## Parallel Example

```
# Launch T010-T012 together:
Task: "Create a service for scraping jobs from LinkedIn in backend/src/services/scraper_linkedin.py"
Task: "Create a service for scraping jobs from Indeed in backend/src/services/scraper_indeed.py"
Task: "Create a service for scraping jobs from Dice in backend/src/services/scraper_dice.py"
```
