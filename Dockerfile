# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for rasterio
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables for rasterio
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy Python scripts from GitHub repo
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    rasterio \
    boto3 \
    logging

# Set default entrypoint
ENTRYPOINT ["python", "process_scene.py"]
