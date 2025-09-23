# API Contract: POST /api/auth/register

## Description
Registers a new user and returns an authentication token.

## Endpoint
`POST /api/auth/register`

## Request
### Headers
- `Content-Type: application/json`

### Body
```json
{
  "username": "string",
  "password": "string",
  "email": "string"
}
```

## Response
### Status Code: 200 OK
### Body
```json
{
  "token": "string"
}