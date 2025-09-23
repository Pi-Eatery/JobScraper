# API Contract: GET /api/applications

## Description
Retrieves a list of job applications for the authenticated user, with optional filtering.

## Endpoint
`GET /api/applications`

## Request
### Headers
- `Authorization: Bearer <token>`

### Query Parameters
- `keywords` (optional): Comma-separated list of keywords to filter by. (Type: String)
- `status` (optional): Filter by application status (e.g., 'Applied', 'Interviewing'). (Type: String)
- `job_board` (optional): Filter by job board (e.g., 'LinkedIn', 'Indeed'). (Type: String)

## Response
### Status Code: 200 OK
### Body
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
  },
  {
    "id": 2,
    "job_title": "Frontend Developer",
    "company": "Web Solutions",
    "application_date": "2023-01-20",
    "status": "Interviewing",
    "job_board": "Indeed",
    "url": "https://indeed.com/jobs/456",
    "notes": "First interview scheduled",
    "keywords": ["react", "javascript"]
  }
]