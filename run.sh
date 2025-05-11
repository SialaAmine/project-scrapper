#!/bin/bash

# Script to build and run the Agoda scraper Docker container

# Build the Docker image
echo "Building Docker image..."
docker-compose build

# Run the container
echo "Starting container..."
docker-compose up

# To run in detached mode, uncomment the following line instead
# docker-compose up -d