# Job Application Tracker

## Description
The "Job Application Tracker" is designed to provide a single authenticated user with a personal platform to efficiently track their job applications. Its primary purpose is to allow users to view, manage, and filter their job applications, while also serving as a robust portfolio project easily shareable with potential employers.

**Key Features:**
*   **Secure Authentication**: User registration and login functionality ensure secure access.
*   **Personalized Application Management**: Display a personalized list of job applications for the logged-in user.
*   **Advanced Filtering**: Ability to filter job applications using keywords and other criteria.
*   **Verified Job Boards**: Ensures job postings are sourced exclusively from "verified good job boards" to prevent scam listings.
*   **Accessibility Compliant**: Adherence to web accessibility standards.
*   **Portfolio Ready**: Designed for easy sharing as a portfolio piece.

**User Roles:**
The primary user role is a single "User" who can log in, manage their job applications, and utilize the filtering capabilities.

## Tech Stack
The project utilizes a modern and robust tech stack for both its frontend and backend components:

*   **Backend**: Python (FastAPI)
*   **Frontend**: React
*   **Database**: SQLite
*   **Containerization**: Docker, Docker Compose
*   **Testing**: Pytest (Python), React Testing Library (React), Jest (React)

## Architecture
The application is designed as a single-user web application, deployed in the cloud. It follows a decoupled architecture with a distinct backend and frontend communicating via a RESTful API. Both components are containerized using Docker, facilitating consistent deployment across different environments.

## Data Model
The project's data model comprises two primary entities:

### User
Represents an individual user of the application.
*   `id`: Primary Key, Integer
*   `username`: Unique String for login
*   `password_hash`: Hashed String for security
*   `email`: String

### JobApplication
Represents a single job application.
*   `id`: Primary Key, Integer
*   `user_id`: Foreign Key, Integer (links to the User entity)
*   `job_title`: String
*   `company`: String
*   `application_date`: Date
*   `status`: String (e.g., Applied, Interviewing, Rejected, Offer, Accepted)
*   `job_board`: String (e.g., LinkedIn, Indeed, Glassdoor)
*   `url`: String (to the job posting)
*   `notes`: Text
*   `keywords`: Array of Strings (for filtering/searching)

**Relationship**:
A one-to-many relationship exists between `User` and `JobApplication`. Each `User` can be associated with multiple `JobApplication` records, and each `JobApplication` is uniquely linked to a single `User` via the `user_id` foreign key.

## Quickstart
This section outlines how to quickly get the Job Application Tracker up and running, including key scenarios for testing and deployment instructions.

### Quickstart Scenarios
These scenarios represent high-level integration tests, demonstrating core user interaction flows:

1.  **User Registration & Login**:
    *   Register a new user account.
    *   Log in with the newly created credentials to obtain an authentication token.
    *   Verify successful access to a protected resource using the obtained token.

2.  **Add and View Job Application**:
    *   Authenticate as a user.
    *   Add a new job application using a POST request to the API.
    *   Retrieve the list of all job applications for the user to confirm the new entry.

3.  **Filter Job Applications**:
    *   Authenticate as a user.
    *   Add multiple job applications with varying keywords, companies, and statuses.
    *   Filter the application list by specific keywords (e.g., "Python", "Frontend") and by status (e.g., "Applied", "Interviewing").
    *   Verify that the filtered results accurately reflect the criteria.

### Deployment Instructions
Follow these steps to deploy the Job Application Tracker:

1.  **Prerequisites**:
    *   Docker and Docker Compose installed.
    *   A Cloudflare account with a configured domain.
    *   Cloudflare Tunnel (`cloudflared`) installed and configured.
    *   Git installed.

2.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/JobScraper.git
    cd JobScraper
    ```
    (Note: Replace `https://github.com/your-username/JobScraper.git` with the actual repository URL)

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory with the following minimum variables:
    ```
    SECRET_KEY="your_super_secret_key"
    DATABASE_URL="sqlite:///./sql_app.db"
    # Add any other necessary backend environment variables
    ```
    (Note: `SECRET_KEY` should be a strong, randomly generated string.)

4.  **Build and Run Docker Containers**:
    Build and start the backend and frontend services using Docker Compose:
    ```bash
    docker-compose up --build -d
    ```
    Verify that the containers are running:
    ```bash
    docker-compose ps
    ```

5.  **Configure Cloudflare Tunnel**:
    *   Authenticate `cloudflared` with your Cloudflare account.
    *   Create a `tunnel.yml` file (e.g., in `~/.cloudflared/` or your preferred location) to define routing for the frontend (port 3000) and backend (port 8000) services.
        Example `tunnel.yml`:
        ```yaml
        tunnel: <YOUR_TUNNEL_UUID>
        credentials-file: /root/.cloudflared/<YOUR_TUNNEL_UUID>.json

        ingress:
          - hostname: frontend.yourdomain.com
            service: http://localhost:3000
          - hostname: backend.yourdomain.com
            service: http://localhost:8000
          - service: http_status:404
        ```
    *   Start the Cloudflare Tunnel:
        ```bash
        cloudflared tunnel run <YOUR_TUNNEL_NAME>
        ```
    *   Ensure that DNS records in your Cloudflare dashboard are configured to point your chosen hostnames (e.g., `frontend.yourdomain.com`, `backend.yourdomain.com`) to the Cloudflare Tunnel.

6.  **Access the Application**:
    *   Access the frontend of the application via `https://frontend.yourdomain.com`.
    *   Access the backend API via `https://backend.yourdomain.com`.

7.  **Continuous Deployment (Optional)**:
    The project can be configured for continuous deployment using GitHub Actions. This automates the build, deployment, and updating of Docker images on your deployment server whenever changes are pushed to the main branch. Refer to the `.github/workflows` directory for examples.