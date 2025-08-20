# Build by 
# ```
# docker build -f api.Dockerfile -t samaapi:development .
# ```

# Run by 
# ```
# docker run -d -p 8000:8000 --name samaapi samaapi:development
# ```

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Gunicorn and other dependencies
RUN pip install --no-cache-dir gunicorn

# Copy requirements first to leverage Docker cache
COPY ./api/requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create static directories
RUN mkdir -p /app/static /app/staticfiles

# Copy project
COPY ./api /app/
COPY ./interpreter /app/interpreter
COPY ./api/check_static.py /app/

# Set proper permissions and collect static files
RUN python check_static.py && \
    python manage.py collectstatic --noinput --clear

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--chdir", "/app", "--workers", "3", "api.wsgi:application"]
