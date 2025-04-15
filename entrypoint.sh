#!/bin/bash

echo "=== Building SAM application ==="
sam build

echo "=== Deploying to AWS ==="
sam deploy \
    --no-confirm-changeset \
    --no-fail-on-empty-changeset \
    --resolve-s3

# Get API endpoint from CloudFormation output
API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name $(cat samconfig.toml | grep stack_name | awk -F '"' '{print $2}') \
    --query 'Stacks[0].Outputs[?OutputKey==`OrdersApiUrl`].OutputValue' \
    --output text)

# Seed Users table
echo "Seeding Users table..."
aws dynamodb put-item \
    --table-name Users \
    --item '{"id": {"S": "test-user-1"}, "name": {"S": "Alice"}}'

aws dynamodb put-item \
    --table-name Users \
    --item '{"id": {"S": "test-user-2"}, "name": {"S": "Bob"}}'

echo "=============================================="
echo "API Endpoint: $API_ENDPOINT"
echo "=============================================="
echo "Test commands:"
echo ""
echo "Create order:"
echo "curl -H \"Authorization: Bearer mock-user-1-token\" -X POST $API_ENDPOINT/orders -H \"Content-Type: application/json\" -d '{\"userId\": \"test-user-2\", \"items\": [{\"productId\": \"head phone\", \"quantity\": 2}, {\"productId\": \"car\", \"quantity\": 1}]}'"
echo ""
echo "List orders:"
echo "curl -H \"Authorization: Bearer mock-user-1-token\" $API_ENDPOINT/orders"
echo ""
echo "Retrieve an order:"
echo "curl -H \"Authorization: Bearer mock-user-1-token\" $API_ENDPOINT/orders/<order_id>"
echo ""
echo "Delete an order:"
echo "curl -H \"Authorization: Bearer mock-user-1-token\" -X DELETE $API_ENDPOINT/orders/<order_id>"
echo ""
echo "=============================================="
echo "To delete the stack later, run: ./destroy.sh"
echo "To exit this container, press Ctrl+C"
echo "=============================================="

# Keep container running
tail -f /dev/null