# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the poetry.lock and pyproject.toml files to the working directory
COPY pyproject.toml poetry.lock ./

# Install poetry
RUN pip install poetry
# Copy the poetry.lock and pyproject.toml files to the working directory
COPY poetry.lock pyproject.toml ./

# Install project dependencies
RUN poetry install --no-root
# Copy the rest of the application code
COPY ./src /app/src

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application using Gunicorn with Uvicorn workers
CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]