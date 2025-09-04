# Use NVIDIA CUDA base image with Python
FROM nvidia/cuda:11.8-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
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