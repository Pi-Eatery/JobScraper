# API Contract: GET /api/applications/{id}

## Description
Retrieves a single job application by its ID for the authenticated user.

## Endpoint
`GET /api/applications/{id}`

## Request
### Headers
- `Authorization: Bearer <token>`

### Path Parameters
- `id`: The unique identifier of the job application. (Type: Integer)

## Response
### Status Code: 200 OK
### Body
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