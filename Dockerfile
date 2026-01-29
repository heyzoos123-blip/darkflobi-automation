# DARKFLOBI AUTOMATION - Production Docker Container
# Multi-stage build for optimized deployment

# Stage 1: Base Python Environment
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    nodejs \
    npm \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome binary path for automation
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_PATH=/usr/bin/chromium

# Stage 2: Application Dependencies
FROM base as deps

WORKDIR /app

# Copy dependency files
COPY requirements.txt package.json ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
RUN npm install

# Stage 3: Production Application
FROM deps as production

# Create non-root user for security
RUN groupadd -r darkflobi && useradd -r -g darkflobi darkflobi

# Copy application code
COPY --chown=darkflobi:darkflobi . /app/

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/temp && \
    chown -R darkflobi:darkflobi /app

# Set up configuration
COPY docker-config/production.env /app/.env

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Switch to non-root user
USER darkflobi

# Expose ports
EXPOSE 8080 3000

# Set working directory
WORKDIR /app

# Default command
CMD ["python3", "deployment/docker-entrypoint.py"]

# ============================================
# MULTI-SERVICE DEPLOYMENT WITH DOCKER COMPOSE
# ============================================

# docker-compose.yml (create this file)
version: '3.8'

services:
  darkflobi-web:
    build: .
    container_name: darkflobi-web
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DARKFLOBI_MODE=web
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    
  darkflobi-automation:
    build: .
    container_name: darkflobi-automation
    environment:
      - NODE_ENV=production
      - DARKFLOBI_MODE=automation
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    depends_on:
      - darkflobi-web
      
  darkflobi-voice:
    build: .
    container_name: darkflobi-voice
    environment:
      - NODE_ENV=production
      - DARKFLOBI_MODE=voice
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
    ports:
      - "3000:3000"
    volumes:
      - ./audio:/app/audio
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: darkflobi-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: darkflobi-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - darkflobi-web
    restart: unless-stopped

volumes:
  redis_data:

networks:
  default:
    name: darkflobi-network