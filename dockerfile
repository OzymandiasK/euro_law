# Use an official Python runtime as the parent image
FROM python:3.9-slim

# Install system dependencies including GDAL and tools to compile Fiona
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Manually specify the version of GDAL installed
# Replace `3.2.0` with the version of libgdal-dev installed above if different
ENV GDAL_VERSION=3.2.0

# Set GDAL and GEOS config paths
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV GEOS_CONFIG=/usr/bin/geos-config

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
COPY data/ /app/data/
COPY eurolaw-883246ae6395.json /app/eurolaw-883246ae6395.json

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY app/ /app/

# Make the Streamlit port available outside this container
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
