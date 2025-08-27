# Dockerfile

# --- Stage 1: Build stage ---
FROM python:3.11-slim-bullseye AS builder

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final stage ---
FROM python:3.11-slim-bullseye AS final

# Set the working directory
WORKDIR /app

# Install Supervisor
RUN apt-get update && apt-get install -y --no-install-recommends supervisor && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy your application code
COPY ./app /app

# Copy the Supervisor configuration file
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Expose the port your FastAPI app will run on
EXPOSE 8000

# The command to run Supervisor, which will in turn start your services
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
