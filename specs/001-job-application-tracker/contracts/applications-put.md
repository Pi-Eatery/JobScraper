# API Contract: PUT /api/applications/{id}

## Description
Updates an existing job application by its ID for the authenticated user.

## Endpoint
`PUT /api/applications/{id}`

## Request
### Headers
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

### Path Parameters
- `id`: The unique identifier of the job application to update. (Type: Integer)

### Body
```json
{
  "job_title": "string (optional)",
  "company": "string (optional)",
  "application_date": "YYYY-MM-DD (optional)",
  "status": "string (optional)",
  "job_board": "string (optional)",
  "url": "string (optional)",
  "notes": "string (optional)",
  "keywords": ["string"] (optional)
}
```

## Response
### Status Code: 200 OK
### Body
```json
{
  "id": 1,
  "job_title": "Software Engineer (Updated)",
  "company": "Tech Corp",
  "application_date": "2023-01-15",
  "status": "Interviewing",
  "job_board": "LinkedIn",
  "url": "https://linkedin.com/jobs/123",
  "notes": "Updated notes",
  "keywords": ["backend", "python"]
}