FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements/ /app/requirements/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements/production.txt

# Copy project
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /var/log/django

# Run migrations and collect static files
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Run entrypoint
CMD ["/app/entrypoint.sh"]
