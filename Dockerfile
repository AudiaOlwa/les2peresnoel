# Use an official Python 3.12 runtime as a parent image
FROM python:3.12-slim-bullseye

# Set environment variables for Python to prevent writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port on which the application will run
EXPOSE 8000

# Set environment variables for Django settings and port
ENV DJANGO_SETTINGS_MODULE=les2peresnoel.settings
ENV PORT=8000

# Run migrations and start the application
CMD ["sh", "-c", "python manage.py migrate && gunicorn les2peresnoel.wsgi:application --bind 0.0.0.0:$PORT"]
