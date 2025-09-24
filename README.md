# Job Application Tracker

## Description
The "Job Application Tracker" is a personal platform designed for a single user to efficiently track job applications. It allows users to view, manage, and filter their job applications, serving as a robust portfolio project.

**Key Features:**
*   **Secure Authentication**: User registration and login functionality.
*   **Personalized Application Management**: Display and manage job applications.
*   **Advanced Filtering**: Filter job applications by keywords and other criteria.

## Tech Stack
*   **Backend**: Python (FastAPI)
*   **Frontend**: React
*   **Database**: SQLite
*   **Containerization**: Docker, Docker Compose
*   **Testing**: Pytest, React Testing Library, Jest

## Quickstart

This section outlines how to quickly get the Job Application Tracker up and running locally.

### Prerequisites:

*   Docker and Docker Compose installed.
*   Git installed.

### Get Started:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/JobScraper.git
    cd JobScraper
    ```
    (Note: Replace `https://github.com/your-username/JobScraper.git` with the actual repository URL)

2.  **Configure Environment Variables**:
    Create a `.env` file in the root directory with the following minimum variables:
    ```
    SECRET_KEY="your_super_secret_key"
    DATABASE_URL="sqlite:///./sql_app.db"
    # Add any other necessary backend environment variables
    ```
    (Note: `SECRET_KEY` should be a strong, randomly generated string.)

3.  **Build and Run Docker Containers**:
    Build and start the backend and frontend services using Docker Compose:
    ```bash
    docker-compose up --build -d
    ```
    Verify that the containers are running:
    ```bash
    docker-compose ps
    ```

4.  **Access the Application**:
    *   The frontend will be available at `http://localhost:3000`.
    *   The backend API will be available at `http://localhost:8000`.

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