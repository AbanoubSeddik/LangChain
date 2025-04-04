# Use Python 3.11 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .

# Create a script to run the application
RUN echo '#!/bin/bash\npython main.py' > /app/run.sh && \
    chmod +x /app/run.sh

# Set the default command (this will be overridden by docker-compose)
CMD ["/app/run.sh"]