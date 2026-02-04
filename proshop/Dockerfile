FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies including PostgreSQL libraries
# libpq5: Required for psycopg2-binary runtime
# libpq-dev: Required for building psycopg2 packages
# gcc, build-essential: For compiling Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq5 \
    libpq-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements/ /app/requirements/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements/production.txt

# Copy project files
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose port (Railway uses PORT env var, but we expose 8000 as default)
EXPOSE 8000

# Run entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

