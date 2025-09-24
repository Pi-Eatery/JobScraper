# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python-is-python3 \
    && rm -rf /var/lib/apt/lists/*

# Install poetry and its dependencies
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

# Set WORKDIR to the backend project root for dependency installation
WORKDIR /app/backend

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY ./src ./src

# Install project dependencies
RUN poetry install --no-root

# Expose the port FastAPI runs on (this should be in the main WORKDIR or handled by Docker Compose)
EXPOSE 8000

# Command to run the application using Uvicorn directly for debugging
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]