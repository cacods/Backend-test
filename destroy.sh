#!/bin/bash

echo "=== Deleting SAM Stack ==="
sam delete --no-prompts

docker-compose down

# Interactive image removal
IMAGE_ID=$(docker images -q backend-test_sam-deployer 2>/dev/null)

if [ -n "$IMAGE_ID" ]; then
  read -p "Do you want to remove the Docker image $IMAGE_ID? [y/N] " -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker rmi $IMAGE_ID
    echo "✓ Removed image $IMAGE_ID"
  else
    echo "✓ Kept image $IMAGE_ID"
  fi
else
  echo "! No SAM deployer image found"
fi
