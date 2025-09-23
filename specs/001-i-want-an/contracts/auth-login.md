# API Contract: POST /api/auth/login

## Description
Authenticates a user and returns an authentication token.

## Endpoint
`POST /api/auth/login`

## Request
### Headers
- `Content-Type: application/json`

### Body
```json
{
  "username": "string",
  "password": "string"
}
```

## Response
### Status Code: 200 OK
### Body
```json
{
  "token": "string"
}