# Quickstart Scenarios for Job Application Tracker

These scenarios outline key user interaction flows and will serve as high-level integration tests to validate the core functionality of the Job Application Tracker.

## Scenario 1: User Registration & Login
### Steps:
1.  **Register a new user**:
    *   **Action**: Send a `POST` request to `/api/auth/register` with a unique `username`, `password`, and `email`.
    *   **Expected Outcome**: Receive a `200 OK` response with an authentication `token`.
2.  **Log in with the new user's credentials**:
    *   **Action**: Send a `POST` request to `/api/auth/login` with the registered `username` and `password`.
    *   **Expected Outcome**: Receive a `200 OK` response with a new authentication `token`.
3.  **Verify successful login**:
    *   **Action**: Attempt to access a protected resource (e.g., `GET /api/applications`) using the received token.
    *   **Expected Outcome**: Receive a `200 OK` response with a list (possibly empty) of job applications.

## Scenario 2: Add and View Job Application
### Steps:
1.  **Log in as an existing user**:
    *   **Action**: Perform steps 1-3 from Scenario 1, or use pre-existing user credentials to obtain a valid authentication token.
    *   **Expected Outcome**: Successfully authenticated with a valid `token`.
2.  **Add a new job application**:
    *   **Action**: Send a `POST` request to `/api/applications` with valid job application data (e.g., `job_title`, `company`, `application_date`, `status`, `job_board`, `url`, `notes`, `keywords`). Include the `Authorization: Bearer <token>` header.
    *   **Expected Outcome**: Receive a `201 Created` response with the details of the newly created job application, including its `id`.
3.  **View the list of job applications and verify the new application is present**:
    *   **Action**: Send a `GET` request to `/api/applications` with the `Authorization: Bearer <token>` header.
    *   **Expected Outcome**: Receive a `200 OK` response containing a list of job applications, and verify that the newly added application is present in the list.

## Scenario 3: Filter Job Applications
### Steps:
1.  **Log in as an existing user**:
    *   **Action**: Perform steps 1-3 from Scenario 1, or use pre-existing user credentials to obtain a valid authentication token.
    *   **Expected Outcome**: Successfully authenticated with a valid `token`.
2.  **Add several job applications with different keywords and statuses**:
    *   **Action**: Send multiple `POST` requests to `/api/applications` with diverse data for `keywords` and `status` fields.
    *   **Expected Outcome**: Receive `201 Created` responses for each application.
3.  **Filter the list by keyword and verify results**:
    *   **Action**: Send a `GET` request to `/api/applications` with `Authorization: Bearer <token>` header and a `keywords` query parameter (e.g., `?keywords=python`).
    *   **Expected Outcome**: Receive a `200 OK` response where all returned job applications contain the specified keyword.
4.  **Filter the list by status and verify results**:
    *   **Action**: Send a `GET` request to `/api/applications` with `Authorization: Bearer <token>` header and a `status` query parameter (e.g., `?status=Interviewing`).
    *   **Expected Outcome**: Receive a `200 OK` response where all returned job applications have the specified status.

## Deployment Instructions

This section outlines the steps to deploy the Job Application Tracker application.

### Prerequisites

*   Docker and Docker Compose installed on your deployment server.
*   A Cloudflare account with a configured domain.
*   Cloudflare Tunnel (`cloudflared`) installed and authenticated on your deployment server.
*   Git installed.

### Steps

1.  **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/JobScraper.git
   cd JobScraper
   ```

2.  **Configure Environment Variables**:
   *   Create a `.env` file in the root directory.
   *   Add necessary environment variables for your backend (e.g., database connection string, secret key for authentication).
       ```
       SECRET_KEY="your_super_secret_key"
       DATABASE_URL="sqlite:///./sql_app.db"
       # Add any other backend specific environment variables
       ```

3.  **Build and Run Docker Containers**:
   *   Navigate to the root of the cloned repository.
   *   Build and start the Docker containers for both backend and frontend:
       ```bash
       docker-compose up --build -d
       ```
   *   Verify that both containers are running:
       ```bash
       docker-compose ps
       ```

4.  **Configure Cloudflare Tunnel**:
   *   Ensure `cloudflared` is authenticated to your Cloudflare account.
   *   Create a `tunnel.yml` configuration file for your Cloudflare Tunnel. This file will define how Cloudflare routes traffic to your Dockerized application.
       ```yaml
       # .cloudflared/tunnel.yml
       tunnel: your-tunnel-id
       credentials-file: /root/.cloudflared/your-tunnel-id.json
       metrics: 0.0.0.0:2006
       ingress:
         - hostname: your-frontend-domain.com
           service: http://localhost:3000 # Frontend service running on port 3000
         - hostname: your-api-domain.com
           service: http://localhost:8000 # Backend service running on port 8000
         - service: http_status:404
       ```
   *   Start the Cloudflare Tunnel:
       ```bash
       cloudflared tunnel run <your-tunnel-name>
       ```
   *   Ensure that DNS records for `your-frontend-domain.com` and `your-api-domain.com` are configured in Cloudflare to proxy through the tunnel.

5.  **Access the Application**:
   *   Once the Docker containers are running and the Cloudflare Tunnel is active, you can access your frontend application at `https://your-frontend-domain.com` and your backend API at `https://your-api-domain.com`.

6.  **Continuous Deployment (Optional)**:
   *   For continuous deployment, set up GitHub Actions (as defined in `.github/workflows/backend_cd.yml` and `.github/workflows/frontend_cd.yml`) to automatically build and deploy new Docker images to a container registry, and then trigger an update on your deployment server.
   *   This typically involves using SSH to connect to your server, pulling the new Docker images, and restarting the `docker-compose` services.