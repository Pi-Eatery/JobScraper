# Quickstart Scenarios for Job Application Tracker

These scenarios outline key user interaction flows and will serve as high-level integration tests to validate the core functionality of the Job Application Tracker.

## Scenario 1: User Registration & Login
### Steps:
1.  **Register a new user**:
    *   **Action**: Send a `POST` request to `/api/auth/register` with a unique `username`, `password`, and `email`.
    *   **Expected Outcome**: Receive a `200 OK` response with an authentication `token`.
2.  **Log in with the new user's credentials**:
    *   **Action**: Send a `POST` request to `/api/auth/login` with the registered `username` and `password`.
    *   **Expected Outcome**: Receive a `200 OK` response with a new authentication `token`.
3.  **Verify successful login**:
    *   **Action**: Attempt to access a protected resource (e.g., `GET /api/applications`) using the received token.
    *   **Expected Outcome**: Receive a `200 OK` response with a list (possibly empty) of job applications.

## Scenario 2: Add and View Job Application
### Steps:
1.  **Log in as an existing user**:
    *   **Action**: Perform steps 1-3 from Scenario 1, or use pre-existing user credentials to obtain a valid authentication token.
    *   **Expected Outcome**: Successfully authenticated with a valid `token`.
2.  **Add a new job application**:
    *   **Action**: Send a `POST` request to `/api/applications` with valid job application data (e.g., `job_title`, `company`, `application_date`, `status`, `job_board`, `url`, `notes`, `keywords`). Include the `Authorization: Bearer <token>` header.
    *   **Expected Outcome**: Receive a `201 Created` response with the details of the newly created job application, including its `id`.
3.  **View the list of job applications and verify the new application is present**:
    *   **Action**: Send a `GET` request to `/api/applications` with the `Authorization: Bearer <token>` header.
    *   **Expected Outcome**: Receive a `200 OK` response containing a list of job applications, and verify that the newly added application is present in the list.

## Scenario 3: Filter Job Applications
### Steps:
1.  **Log in as an existing user**:
    *   **Action**: Perform steps 1-3 from Scenario 1, or use pre-existing user credentials to obtain a valid authentication token.
    *   **Expected Outcome**: Successfully authenticated with a valid `token`.
2.  **Add several job applications with different keywords and statuses**:
    *   **Action**: Send multiple `POST` requests to `/api/applications` with diverse data for `keywords` and `status` fields.
    *   **Expected Outcome**: Receive `201 Created` responses for each application.
3.  **Filter the list by keyword and verify results**:
    *   **Action**: Send a `GET` request to `/api/applications` with `Authorization: Bearer <token>` header and a `keywords` query parameter (e.g., `?keywords=python`).
    *   **Expected Outcome**: Receive a `200 OK` response where all returned job applications contain the specified keyword.
4.  **Filter the list by status and verify results**:
    *   **Action**: Send a `GET` request to `/api/applications` with `Authorization: Bearer <token>` header and a `status` query parameter (e.g., `?status=Interviewing`).
    *   **Expected Outcome**: Receive a `200 OK` response where all returned job applications have the specified status.