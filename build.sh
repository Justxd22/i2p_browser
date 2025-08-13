#!/bin/bash

set -e

echo "Building Firefox with i2pd integration..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Build the image
echo "Building Docker image..."
docker build -t firefox-i2pd .
docker run -it -p 5800:5800 firefox-i2pd 

docker tag i2pd-firefox tqwee/i2pd-firefox:latest
