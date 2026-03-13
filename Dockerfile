# INFRAS-CLOUD Dockerfile
# Atmospheric Infrasound & Severe Weather Acoustic Signatures
# Version: 1.0.0 | DOI: 10.5281/zenodo.18952438

FROM python:3.10-slim as builder

LABEL maintainer="Samir Baladi <gitdeeper@gmail.com>"
LABEL description="INFRAS-CLOUD: Atmospheric Infrasound & Severe Weather Acoustic Signatures"
LABEL version="1.0.0"
LABEL doi="10.5281/zenodo.18952438"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    gfortran \
    libhdf5-dev \
    libnetcdf-dev \
    libfftw3-dev \
    libusb-1.0-0-dev \
    libatlas-base-dev \
    libopenblas-dev \
    git \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /build

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# ============================================
# Final stage
# ============================================
FROM python:3.10-slim

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libhdf5-103 \
    libnetcdf19 \
    libfftw3-3 \
    libusb-1.0-0 \
    libatlas3-base \
    libopenblas0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Create app directory
WORKDIR /app

# Copy application code
COPY infrascloud/ ./infrascloud/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY web/ ./web/
COPY dashboard/ ./dashboard/
COPY models/ ./models/
COPY .env.example ./
COPY setup.py setup.cfg pyproject.toml MANIFEST.in ./
COPY README.md LICENSE CHANGELOG.md AUTHORS.md ./

# Create necessary directories
RUN mkdir -p /data/raw /data/processed /data/aisi /data/events /logs /config

# Create non-root user
RUN useradd -m -u 1000 infrauser && \
    chown -R infrauser:infrauser /app /data /logs /config

USER infrauser

# Set environment variables
ENV PYTHONPATH=/app:$PYTHONPATH \
    INFRA_HOME=/app \
    INFRA_DATA=/data \
    INFRA_CONFIG=/config \
    INFRA_LOGS=/logs

# Expose ports
EXPOSE 5000 8000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Set entrypoint
ENTRYPOINT ["infrascloud"]

# Default command
CMD ["serve", "--host", "0.0.0.0", "--port", "5000"]
