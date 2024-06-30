# Use the official Python image from the Docker Hub
FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Copy requirements and install production dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /usr/src/app/

# Expose the port the app runs on
EXPOSE 8000

# Define the final stage for production
FROM base AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Copy the production files from base stage
COPY --from=base /usr/src/app /usr/src/app

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]

# Define the development stage
FROM base AS development

# Install development dependencies
COPY requirements-dev.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements-dev.txt

# Command for running development server or tests
CMD ["pytest"]

