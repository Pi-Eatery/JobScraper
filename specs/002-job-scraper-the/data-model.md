# Data Model

## Entities

### User
Represents a user of the application.

**Attributes**:
- `id`: Unique identifier (PK)
- `username`: String
- `password`: Hashed string

### Job
Represents a job posting scraped from an online source.

**Attributes**:
- `id`: Unique identifier (PK)
- `title`: String
- `company`: String
- `description`: String
- `application_link`: String (required)
- `salary`: String (optional)
- `status`: String (e.g., 'new', 'saved', 'applied', 'hidden')
- `user_id`: Foreign key to User

### Keyword
Represents a search term used to filter jobs.

**Attributes**:
- `id`: Unique identifier (PK)
- `term`: String

## Relationships
- A **User** can have many **Jobs**.
- A **Job** belongs to one **User**.
