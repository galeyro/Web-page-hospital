# Stage 1: Build the React frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the Django backend
FROM python:3.11-slim
WORKDIR /app/hospital

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY hospital/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY hospital/ ./

# Copy built frontend dist from Stage 1 into the location expected by Django
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose Django port
EXPOSE 8000

# Create folder for database with open permissions so that it works as a volume mount
RUN mkdir -p /data && chmod 777 /data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000"

# Fix CRLF line endings if built on Windows and make startup script executable
RUN sed -i 's/\r$//' startup.sh && chmod +x startup.sh

CMD ["./startup.sh"]
