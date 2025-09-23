<!--
Version change: None (initial creation) -> 0.1.0
List of modified principles:
    - PRINCIPLE_1_NAME -> I. Security by Design
    - PRINCIPLE_2_NAME -> II. Automated Testing & Quality Gates
    - PRINCIPLE_3_NAME -> III. Infrastructure as Code (IaC)
    - PRINCIPLE_4_NAME -> IV. Observability & Monitoring
    - PRINCIPLE_5_NAME -> V. Continuous Delivery & Deployment (CD)
Added sections:
    - Development Environment & Tooling
    - DevSecOps Best Practices
Removed sections:
    - SECTION_2_NAME, SECTION_2_CONTENT (replaced by specific content)
    - SECTION_3_NAME, SECTION_3_CONTENT (replaced by specific content)
Templates requiring updates:
    - .specify/templates/plan-template.md: ✅ updated
    - .specify/templates/spec-template.md: ✅ updated
    - .specify/templates/tasks-template.md: ✅ updated
    - .specify/templates/commands/*.md: ✅ updated (no files found in directory)
Follow-up TODOs: None
-->
# Containerized Python Application Constitution

## Core Principles

### I. Security by Design
Security considerations are integrated into every stage of the software development lifecycle, from initial design to deployment and operations. This includes threat modeling, secure coding practices, and proactive vulnerability scanning.

### II. Automated Testing & Quality Gates
Comprehensive automated testing (unit, integration, end-to-end) is mandatory for all code changes. Quality gates, including static analysis, dynamic analysis, and security scans, must pass before deployment to ensure code quality and identify vulnerabilities early.

### III. Infrastructure as Code (IaC)
All infrastructure components, including application environments, network configurations (e.g., Cloudflare Tunnels), and server setups, are defined and managed as code. This ensures consistency, repeatability, and version control for infrastructure changes, adhering to GitOps principles.

### IV. Observability & Monitoring
Applications must be designed with comprehensive observability in mind, including structured logging, metrics, and tracing. Centralized monitoring and alerting are implemented to quickly detect, diagnose, and resolve operational issues, ensuring application health and performance.

### V. Continuous Delivery & Deployment (CD)
Automated pipelines ensure reliable and efficient delivery of software to production. Deployments are frequent, small, and reversible, enabling rapid iteration and minimizing risk. Cloudflare Tunnels are leveraged for secure and efficient remote access to deployed applications.

## Development Environment & Tooling

All development activities will utilize containerization (Docker) to ensure consistent environments across development, testing, and production. Python is the primary development language. Cloudflare Tunnels are used for secure remote access to development and production instances. All changes must go through version control (Git) and adhere to a peer review process.

## DevSecOps Best Practices

DevSecOps best practices are embedded throughout the entire software delivery pipeline. This includes:
- **Shift-Left Security:** Integrating security scans (SAST, DAST, dependency scanning) early in the development process.
- **Supply Chain Security:** Verifying the integrity of all third-party dependencies and container images.
- **Least Privilege:** Implementing the principle of least privilege for all users, services, and infrastructure components.
- **Immutable Infrastructure:** Favoring immutable infrastructure patterns to reduce configuration drift and enhance security.
- **Automated Security Controls:** Leveraging automation to enforce security policies and respond to threats.

## Governance
This constitution supersedes all other practices. Amendments require a formal proposal, peer review, and approval by at least two senior engineers. All pull requests and code reviews must explicitly verify compliance with these principles. New features or significant changes must include an architectural decision record (ADR) detailing how they adhere to the constitution.

**Version**: 0.1.0 | **Ratified**: 2025-09-22 | **Last Amended**: 2025-09-22