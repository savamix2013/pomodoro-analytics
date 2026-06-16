FROM python:3.13-slim

WORKDIR /app

# Install system dependencies and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies with verbose output for debugging
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --verbose 2>&1 | head -100

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "-c", "gunicorn.conf.py"]
