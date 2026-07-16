# DFM Inspector - production container
#
# Builds a minimal Linux image with the app and its Python dependencies.
# Uses gunicorn as the WSGI server (Flask's dev server is not for production).
#
# Build:   docker build -t dfm-inspector .
# Run:     docker run -p 5000:5000 dfm-inspector
# Health:  curl http://localhost:5000/health
#
# Image size target: ~500MB. The bulk is matplotlib + scikit-learn + numpy.

FROM python:3.11-slim AS base

# System libs needed by matplotlib (font rendering), trimesh (binary mesh
# I/O), and rtree (libspatialindex). Kept to a minimal set.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libspatialindex-dev \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Run as a non-root user. Containers should never run as root by default.
RUN useradd --create-home --shell /bin/bash --uid 1000 dfm

WORKDIR /app

# Install Python deps first so they're cached across code-only rebuilds.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir gunicorn==21.2.0

# Copy the application code.
COPY app.py /app/app.py
COPY src/ /app/src/
COPY templates/ /app/templates/
COPY rules/ /app/rules/

# Drop privileges.
USER dfm

# Gunicorn config:
#   - 2 workers: small enough for App Runner's smallest size, large enough
#     to handle a couple of concurrent uploads. Increase via env if needed.
#   - 300s timeout: STEP analysis can take a while on large parts.
#   - access log to stdout so it shows up in CloudWatch.
ENV PORT=80 \
    GUNICORN_WORKERS=2 \
    GUNICORN_TIMEOUT=300 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 80

# /health is provided by app.py via gunicorn's WSGI; no extra endpoint
# wiring needed because we add it in app.py below.
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:80/health',timeout=5).status==200 else 1)" \
        || exit 1

CMD ["sh", "-c", "gunicorn --workers=${GUNICORN_WORKERS} --timeout=${GUNICORN_TIMEOUT} --bind=0.0.0.0:${PORT} --access-logfile=- --error-logfile=- app:app"]
