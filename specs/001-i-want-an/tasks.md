# Tasks: Job Application Tracker

**Input**: Design documents from `/specs/001-i-want-an/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web application structure based on plan.md

## Phase 3.1: Setup
- [x] T001 Create backend/ and frontend/ project directories
- [x] T002 Initialize Python backend project (e.g., FastAPI) in `backend/`
- [x] T003 [P] Initialize React frontend project in `frontend/`
- [x] T004 Install backend dependencies (e.g., `SQLAlchemy`, `FastAPI`, `uvicorn`) in `backend/`
- [x] T005 [P] Install frontend dependencies (e.g., `react-router-dom`, `axios`) in `frontend/`
- [x] T006 [P] Configure backend linting (`Bandit`) and formatting (`Black`)
- [x] T007 [P] Configure frontend linting (`ESLint`) and formatting (`Prettier`)
- [x] T008 Commit "Initial project setup and configuration"

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### Contract Tests (Backend)
- [x] T009 [P] Contract test `POST /api/auth/register` in `backend/tests/contract/test_auth_register.py`
- [x] T010 [P] Contract test `POST /api/auth/login` in `backend/tests/contract/test_auth_login.py`
- [x] T011 [P] Contract test `POST /api/applications` in `backend/tests/contract/test_applications_post.py`
- [x] T012 [P] Contract test `GET /api/applications` in `backend/tests/contract/test_applications_get_all.py`
- [x] T013 [P] Contract test `GET /api/applications/{id}` in `backend/tests/contract/test_applications_get_by_id.py`
- [x] T014 [P] Contract test `PUT /api/applications/{id}` in `backend/tests/contract/test_applications_put.py`
- [x] T015 [P] Contract test `DELETE /api/applications/{id}` in `backend/tests/contract/test_applications_delete.py`

### Integration Tests (Quickstart Scenarios)
- [x] T016 [P] Integration test user registration and login (`Scenario 1`) in `backend/tests/integration/test_user_auth.py`
- [x] T017 [P] Integration test add and view job application (`Scenario 2`) in `backend/tests/integration/test_applications_crud.py`
- [x] T018 [P] Integration test filter job applications (`Scenario 3`) in `backend/tests/integration/test_applications_filter.py`
- [x] T019 Git: Commit "Add all failing contract and integration tests" (`git add . && git commit -m "Add all failing contract and integration tests" && git push origin main`)

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Backend (Python)
- [x] T020 Create `User` model in `backend/src/models/user.py`
- [x] T021 Create `JobApplication` model in `backend/src/models/job_application.py`
- [x] T022 Implement database connection and session management in `backend/src/models/database.py`
- [x] T023 Implement `User` authentication service (register, login) in `backend/src/services/auth_service.py`
- [x] T024 Implement `JobApplication` CRUD service in `backend/src/services/application_service.py`
- [x] T025 Implement authentication routes (`/api/auth/register`, `/api/auth/login`) in `backend/src/api/auth.py`
- [x] T026 Implement job application routes (`/api/applications`, `/api/applications/{id}`) in `backend/src/api/applications.py`
- [x] T027 Implement input validation for all API endpoints in `backend/src/schemas/`
- [x] T028 Implement global error handling and structured logging (`Python logging`) in `backend/src/main.py`
 
 ### Frontend (React)
 - [x] T029 Create React components for user registration and login forms in `frontend/src/components/auth/`
 - [x] T030 Implement user authentication context/provider in `frontend/src/context/AuthContext.js`
 - [x] T031 Create React component to display job application list in `frontend/src/components/applications/ApplicationList.js`
 - [x] T032 Implement job application filtering UI in `frontend/src/components/applications/ApplicationFilter.js`
 - [x] T033 Create React components for adding, editing, and deleting job applications in `frontend/src/components/applications/ApplicationForm.js`
 - [x] T034 Implement data fetching and state management for job applications in `frontend/src/services/api.js`
 - [x] T035 Implement basic routing for login, register, and application list pages in `frontend/src/App.js`
- [x] T036 Git: Commit "Implement core backend and frontend features" (`git add . && git commit -m "Implement core backend and frontend features" && git push origin main`)

## Phase 3.4: Integration
- [ ] T037 Configure backend to connect to SQLite database
- [ ] T038 Implement authentication middleware for protected backend routes in `backend/src/middleware/auth.py`
- [ ] T039 Configure CORS for frontend/backend communication
- [ ] T040 Set up Dockerfile for backend in `backend/Dockerfile`
- [ ] T041 Set up Dockerfile for frontend in `frontend/Dockerfile`
- [ ] T042 Create `docker-compose.yml` to run backend and frontend containers
- [ ] T043 Integrate Prometheus Node Exporter for Docker container metrics
- [ ] T044 Create `.github/workflows/backend_ci.yml` for backend CI (lint, test, build)
- [ ] T045 Create `.github/workflows/frontend_ci.yml` for frontend CI (lint, test, build)
- [ ] T046 Git: Commit "Integrate services, Docker, and initial CI workflows" (`git add . && git commit -m "Integrate services, Docker, and initial CI workflows" && git push origin main`)

## Phase 3.5: Polish
- [ ] T047 [P] Implement unit tests for backend models and services in `backend/tests/unit/`
- [ ] T048 [P] Implement unit tests for frontend components and utilities in `frontend/src/tests/`
- [ ] T049 Add performance testing for key API endpoints
- [ ] T050 Update `quickstart.md` with deployment instructions
- [ ] T051 Ensure accessibility standards are met for frontend components
- [ ] T052 [P] Integrate `Docker Scout` for container image scanning in CI/CD
- [ ] T053 [P] Implement `pip-audit` for dependency vulnerability checks in CI/CD
- [ ] T054 Refine GitHub Actions workflow for CD (deploy to Linux server via Cloudflare Tunnels) in `.github/workflows/backend_cd.yml` and `.github/workflows/frontend_cd.yml`
- [ ] T055 Git: Commit "Final polish, tests, and CI/CD refinements" (`git add . && git commit -m "Final polish, tests, and CI/CD refinements" && git push origin main`)

## Dependencies
- Setup tasks (T001-T008) before any other tasks.
- Tests (T009-T019) before Core Implementation (T020-T036).
- Backend models (T020-T021) before backend services (T023-T024) and API routes (T025-T026).
- Backend services (T023-T024) before API routes (T025-T026).
- Frontend components (T029, T031, T032, T033) can be developed in parallel, but depend on API services.
- Integration tasks (T037-T046) depend on core implementation.
- Polish tasks (T047-T055) can run after core implementation and tests, with some parallelization.

## Parallel Example
```
# Phase 3.1: Setup - can run in parallel
Task: "T003 [P] Initialize React frontend project in `frontend/`"
Task: "T004 Install backend dependencies (e.g., `SQLAlchemy`, `FastAPI`, `uvicorn`) in `backend/`"
Task: "T005 [P] Install frontend dependencies (e.g., `react-router-dom`, `axios`) in `frontend/`"
Task: "T006 [P] Configure backend linting (`Bandit`) and formatting (`Black`)"
Task: "T007 [P] Configure frontend linting (`ESLint`) and formatting (`Prettier`)"

# Phase 3.2: Tests First (TDD) - can run in parallel
Task: "T009 [P] Contract test POST /api/auth/register in backend/tests/contract/test_auth_register.py"
Task: "T010 [P] Contract test POST /api/auth/login in backend/tests/contract/test_auth_login.py"
Task: "T011 [P] Contract test POST /api/applications in backend/tests/contract/test_applications_post.py"
Task: "T012 [P] Contract test GET /api/applications in backend/tests/contract/test_applications_get_all.py"
Task: "T013 [P] Contract test GET /api/applications/{id} in backend/tests/contract/test_applications_get_by_id.py"
Task: "T014 [P] Contract test PUT /api/applications/{id} in backend/tests/contract/test_applications_put.py"
Task: "T015 [P] Contract test DELETE /api/applications/{id} in backend/tests/contract/test_applications_delete.py"
Task: "T016 [P] Integration test user registration and login (Scenario 1) in backend/tests/integration/test_user_auth.py"
Task: "T017 [P] Integration test add and view job application (Scenario 2) in backend/tests/integration/test_applications_crud.py"
Task: "T018 [P] Integration test filter job applications (Scenario 3) in backend/tests/integration/test_applications_filter.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests
- [x] All entities have model tasks
- [x] All tests come before implementation
- [x] Parallel tasks truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task