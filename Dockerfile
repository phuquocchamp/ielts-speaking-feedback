FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src

# Set default port (can be overridden)
ENV PORT=8000

# Expose port
EXPOSE ${PORT}

# Command to run the application
CMD uvicorn src.api.handler:app --host 0.0.0.0 --port ${PORT}
