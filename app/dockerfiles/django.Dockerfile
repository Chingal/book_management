# Base image for building dependencies
FROM python:3.10-alpine as builder

# Enviroment variables and Args.
ARG DJANGO_ENV

# Set working directory
WORKDIR /app

# Install system packages
RUN apk add --no-cache --upgrade gcc netcat-openbsd

# Copy requirements
COPY requirements /app/requirements

# Install application dependencies
RUN pip install --upgrade pip && pip install -r requirements/$DJANGO_ENV.txt

# Base image for running the application
FROM python:3.10-alpine

# Copy dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/celery /usr/local/bin/celery
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Create non-privileged user
RUN adduser --disabled-password --gecos '' app

# Set working directory
WORKDIR /app

ENV HOME /home/app

# Copy application
COPY . /app

RUN chown -R app /app

# Run the application using the script
CMD ["sh", "./scripts/app.sh"]

# Gunicorn listening port
EXPOSE 8007/tcp

USER app