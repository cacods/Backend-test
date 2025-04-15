#!/bin/bash

# Build and run the container
docker-compose up --build

echo "Container is running in detached mode."
echo "To attach to the container: docker attach sam-deployer"
echo "To stop the container: docker-compose down"