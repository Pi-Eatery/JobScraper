# Contract Tests for Job Application Tracker API

These tests are designed to verify that the API endpoints adhere to their defined contracts (request/response schemas, HTTP methods, and paths). These tests are expected to *fail* initially as the API implementation does not yet exist.

## User Authentication

### Test: POST /api/auth/login
- **Description**: Verify the contract for user login.
- **Method**: POST
- **Endpoint**: `/api/auth/login`
- **Request Body**:
  ```json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```
- **Expected Response (200 OK)**:
  ```json
  {
    "token": "expected_jwt_token_format_string"
  }
  ```
- **Assertions**:
  - HTTP Status Code is 200.
  - Response body matches the `auth-login.md` schema, containing a 'token' string.

### Test: POST /api/auth/register
- **Description**: Verify the contract for user registration.
- **Method**: POST
- **Endpoint**: `/api/auth/register`
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "password": "newpassword",
    "email": "newuser@example.com"
  }
  ```
- **Expected Response (200 OK)**:
  ```json
  {
    "token": "expected_jwt_token_format_string"
  }
  ```
- **Assertions**:
  - HTTP Status Code is 200.
  - Response body matches the `auth-register.md` schema, containing a 'token' string.

## Job Applications

### Test: GET /api/applications
- **Description**: Verify the contract for retrieving all job applications.
- **Method**: GET
- **Endpoint**: `/api/applications`
- **Headers**: `Authorization: Bearer <valid_token>`
- **Query Parameters**:
  - `keywords`: "backend,python"
  - `status`: "Applied"
  - `job_board`: "LinkedIn"
- **Expected Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "job_title": "Software Engineer",
      "company": "Tech Corp",
      "application_date": "2023-01-15",
      "status": "Applied",
      "job_board": "LinkedIn",
      "url": "https://linkedin.com/jobs/123",
      "notes": "Initial application",
      "keywords": ["backend", "python"]
    }
  ]
  ```
- **Assertions**:
  - HTTP Status Code is 200.
  - Response body is an array of job application objects, each matching the schema defined in `applications-get-all.md`.
  - Filtering parameters are respected.

### Test: GET /api/applications/{id}
- **Description**: Verify the contract for retrieving a single job application by ID.
- **Method**: GET
- **Endpoint**: `/api/applications/{id}` (e.g., `/api/applications/1`)
- **Headers**: `Authorization: Bearer <valid_token>`
- **Path Parameters**: `id` = 1
- **Expected Response (200 OK)**:
  ```json
  {
    "id": 1,
    "job_title": "Software Engineer",
    "company": "Tech Corp",
    "application_date": "2023-01-15",
    "status": "Applied",
    "job_board": "LinkedIn",
    "url": "https://linkedin.com/jobs/123",
    "notes": "Initial application",
    "keywords": ["backend", "python"]
  }
  ```
- **Assertions**:
  - HTTP Status Code is 200.
  - Response body matches the `applications-get-by-id.md` schema.

### Test: POST /api/applications
- **Description**: Verify the contract for creating a new job application.
- **Method**: POST
- **Endpoint**: `/api/applications`
- **Headers**: `Authorization: Bearer <valid_token>`
- **Request Body**:
  ```json
  {
    "job_title": "New Job",
    "company": "New Company",
    "application_date": "2023-09-23",
    "status": "Applied",
    "job_board": "Indeed",
    "url": "https://indeed.com/newjob",
    "notes": "Applied online",
    "keywords": ["devops", "cloud"]
  }
  ```
- **Expected Response (201 Created)**:
  ```json
  {
    "id": 1,
    "job_title": "New Job",
    "company": "New Company",
    "application_date": "2023-09-23",
    "status": "Applied",
    "job_board": "Indeed",
    "url": "https://indeed.com/newjob",
    "notes": "Applied online",
    "keywords": ["devops", "cloud"]
  }
  ```
- **Assertions**:
  - HTTP Status Code is 201.
  - Response body matches the `applications-post.md` schema, including a generated `id`.

### Test: PUT /api/applications/{id}
- **Description**: Verify the contract for updating an existing job application.
- **Method**: PUT
- **Endpoint**: `/api/applications/{id}` (e.g., `/api/applications/1`)
- **Headers**: `Authorization: Bearer <valid_token>`
- **Path Parameters**: `id` = 1
- **Request Body**:
  ```json
  {
    "status": "Interviewing",
    "notes": "Scheduled for interview"
  }
  ```
- **Expected Response (200 OK)**:
  ```json
  {
    "id": 1,
    "job_title": "Software Engineer",
    "company": "Tech Corp",
    "application_date": "2023-01-15",
    "status": "Interviewing",
    "job_board": "LinkedIn",
    "url": "https://linkedin.com/jobs/123",
    "notes": "Scheduled for interview",
    "keywords": ["backend", "python"]
  }
  ```
- **Assertions**:
  - HTTP Status Code is 200.
  - Response body matches the `applications-put.md` schema, with updated fields.

### Test: DELETE /api/applications/{id}
- **Description**: Verify the contract for deleting a job application.
- **Method**: DELETE
- **Endpoint**: `/api/applications/{id}` (e.g., `/api/applications/1`)
- **Headers**: `Authorization: Bearer <valid_token>`
- **Path Parameters**: `id` = 1
- **Expected Response (200 OK)**:
  ```json
  {
    "message": "Application deleted"
  }
  ```
- **Assertions**:
  - HTTP Status Code is 200.
  - Response body matches the `applications-delete.md` schema.