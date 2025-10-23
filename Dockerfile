FROM python:3.11-slim

# Set workdir
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build deps and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt gunicorn

# Copy project
COPY . /app

# Ensure upload folder exists
RUN mkdir -p /app/static/images

EXPOSE 8000

# Use gunicorn to serve the Flask app (app:app)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
