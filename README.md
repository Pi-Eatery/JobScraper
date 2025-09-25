# Job Application Tracker

## Description
The "Job Application Tracker" is a personal platform designed for a single user to efficiently track job applications. It allows users to view, manage, and filter their job applications, serving as a robust portfolio project.

**Key Features:**
*   **Secure Authentication**: User registration and login functionality.
*   **Personalized Application Management**: Display and manage job applications.
*   **Advanced Filtering**: Filter job applications by keywords and other criteria.
*   **Automated Job Scraping**: Automatically scrape job postings from various platforms.

## Tech Stack
*   **Backend**: Python (FastAPI), BeautifulSoup, Scrapy
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
    REACT_APP_API_BASE_URL="http://192.168.2.201:8000/api" # The URL where the frontend will access the backend API. Adjust IP as needed.
    CORS_ORIGINS="http://192.168.2.201:3000" # The origin(s) allowed to make requests to the backend. Adjust IP as needed.
    ```
    (Note: `SECRET_KEY` should be a strong, randomly generated string. `REACT_APP_API_BASE_URL` and `CORS_ORIGINS` should reflect the IP address where your frontend is served and where your backend is exposed.)

3.  **Build and Run Docker Containers**:
    Build and start the backend and frontend services using Docker Compose:
    ```bash
    docker compose up --build -d
    ```
    Verify that the containers are running:
    ```bash
    docker compose ps
    ```

4.  **Access the Application**:
    *   The frontend will be available at `http://localhost:3000`.
    *   The backend API will be available at `http://localhost:8000`.

### Configuring Non-Standard Ports

If you wish to use non-standard ports for the application, you will need to modify the following files:

1.  **[`docker-compose.yml`](docker-compose.yml)**:
    Update the `ports` mapping for both the `frontend` and `backend` services.
    *   **Frontend**: Change `3000:80` to `YOUR_FRONTEND_PORT:80`.
    *   **Backend**: Change `8000:8000` to `YOUR_BACKEND_PORT:8000`.

    Example:
    ```yaml
    frontend:
      ports:
        - "8080:80" # Maps host port 8080 to container's port 80 (Nginx default)
    backend:
      ports:
        - "8081:8000" # Maps host port 8081 to container's port 8000 (FastAPI default)
    ```

2.  **Cloudflare Tunnel Configuration (`tunnel.yml`)** (if used):
    If you are using Cloudflare Tunnel, update the `service` entries in your `tunnel.yml` to reflect the new host ports.

    Example `tunnel.yml` (after changing ports in `docker-compose.yml` to `8080` and `8081`):
    ```yaml
    ingress:
      - hostname: frontend.yourdomain.com
        service: http://localhost:8080
      - hostname: backend.yourdomain.com
        service: http://localhost:8081
      - service: http_status:404
    ```

After making these changes, remember to rebuild and restart your Docker containers:
```bash
docker compose up --build -d
```
And restart your `cloudflared` tunnel if you modified `tunnel.yml`.

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