# Data Model: Job Application Tracker

## Entities

### User
- **id**: Primary Key, Unique identifier for the user. (Type: Integer)
- **username**: Unique username for login. (Type: String)
- **password_hash**: Hashed password for security. (Type: String)
- **email**: User's email address. (Type: String)

### JobApplication
- **id**: Primary Key, Unique identifier for the job application. (Type: Integer)
- **user_id**: Foreign Key, References the User's id. (Type: Integer)
- **job_title**: Title of the job applied for. (Type: String)
- **company**: Company name. (Type: String)
- **application_date**: Date when the application was submitted. (Type: Date)
- **status**: Current status of the application (e.g., Applied, Interviewing, Rejected, Offer, Accepted). (Type: String)
- **job_board**: The platform where the job was found (e.g., LinkedIn, Indeed, Glassdoor). (Type: String)
- **url**: URL to the original job posting. (Type: String)
- **notes**: Any additional notes about the application. (Type: Text)
- **keywords**: Relevant keywords for filtering/searching. (Type: Array of Strings)