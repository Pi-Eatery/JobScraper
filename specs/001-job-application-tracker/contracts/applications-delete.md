# API Contract: DELETE /api/applications/{id}

## Description
Deletes a job application by its ID for the authenticated user.

## Endpoint
`DELETE /api/applications/{id}`

## Request
### Headers
- `Authorization: Bearer <token>`

### Path Parameters
- `id`: The unique identifier of the job application to delete. (Type: Integer)

## Response
### Status Code: 200 OK
### Body
```json
{
  "message": "Application deleted"
}