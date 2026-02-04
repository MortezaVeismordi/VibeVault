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

# Copy requirements from proshop directory
COPY proshop/requirements/ /app/requirements/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements/production.txt

# Copy project files from proshop directory
# This copies everything inside proshop/ directly to /app/
# So /app/manage.py exists, /app/entrypoint.sh exists
COPY proshop/ /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Health check (using curl if available, otherwise simplified check)
# Since we didn't install curl, we'll rely on the simplified check or just remove it to rely on platform health checks
# But let's keep the simple python check just in case
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import http.client; conn = http.client.HTTPConnection('localhost', 8000); conn.request('GET', '/admin/login/'); response = conn.getresponse(); exit(0) if response.status < 500 else exit(1)" || exit 1

# Run entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
