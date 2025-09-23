# API Contract: POST /api/applications

## Description
Creates a new job application for the authenticated user.

## Endpoint
`POST /api/applications`

## Request
### Headers
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

### Body
```json
{
  "job_title": "string",
  "company": "string",
  "application_date": "YYYY-MM-DD",
  "status": "string",
  "job_board": "string",
  "url": "string",
  "notes": "string",
  "keywords": ["string"]
}
```

## Response
### Status Code: 201 Created
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