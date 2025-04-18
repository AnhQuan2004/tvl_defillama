#!/bin/bash

# Build the Docker image defined in docker-compose.yml
echo "Building Docker image..."
docker-compose build

# Start the services defined in docker-compose.yml in detached mode
echo "Starting services..."
docker-compose up -d

echo "Deployment finished. Service should be running on port 5000." 