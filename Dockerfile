FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system libraries needed by dlib (C++ / CMake) and librosa/audio (libsndfile, ffmpeg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libopenblas-dev \
    libx11-dev \
    libsndfile1 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces security: create and run as non-root user (UID 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Copy requirements and install dependencies into user home
COPY --chown=user:user backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY --chown=user:user backend/ /app/backend/

# Hugging Face Spaces listens on port 7860 by default
EXPOSE 7860

# Start Uvicorn on 0.0.0.0 and port 7860 (or $PORT if specified)
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]

