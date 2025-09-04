# Use Ubuntu 22.04 as base image
FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-runtime

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies including Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic link for python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Hugging Face
ENV HF_HOME=/app/cache
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_HUB_CACHE=/app/cache
ENV HF_DATASETS_CACHE=/app/cache

# Create cache directory for Hugging Face models
RUN mkdir -p /app/cache

# Copy model download script and run it
COPY download_model.py .
RUN python download_model.py

# Copy application code
COPY handler.py .

# Expose port (optional, for debugging)
EXPOSE 8000

# Command to run the application
CMD ["python", "handler.py"]