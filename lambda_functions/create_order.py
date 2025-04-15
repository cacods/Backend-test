import json
import os

from datetime import datetime
from uuid import uuid4

import boto3

from botocore.exceptions import ClientError

try:
    # If running locally, import from the parent directory
    from lambda_functions.auth import InvalidTokenException, validate_token
except ImportError:
    from auth import InvalidTokenException, validate_token


def lambda_handler(event, context):
    """Create a new order.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (LambdaContext): The context object provided by AWS Lambda.

    Returns:
        dict: The response object containing the status code and body.

    Raises:
        InvalidTokenException: If the provided token is invalid.
        ValueError: If the request body is invalid.
        ClientError: If there is an error creating the order in DynamoDB.
    """
    auth_token = event.get("headers", {}).get("Authorization")
    try:
        validate_token(auth_token)
    except InvalidTokenException as e:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": str(e)}),
        }

    dynamodb = boto3.resource("dynamodb")
    users_table = dynamodb.Table(os.getenv("USERS_TABLE"))
    orders_table = dynamodb.Table(os.getenv("ORDERS_TABLE"))

    body = json.loads(event["body"])
    try:
        _validate_body(body)
    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
        }

    user_id = body["userId"]

    response = users_table.get_item(Key={"id": user_id})
    if "Item" not in response:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "User not found"}),
        }

    order_id = str(uuid4())
    try:
        orders_table.put_item(
            Item={
                "id": order_id,
                "userId": user_id,
                "items": body["items"],
                "status": "created",
                "createdAt": datetime.now().isoformat(),
            }
        )
    except ClientError as e:
        print(f"Error creating order: {e}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
        }

    return {
        "statusCode": 201,
        "body": json.dumps({"id": order_id}),
    }


def _validate_body(body):
    """Validate the request body."""
    if "userId" not in body or "items" not in body:
        raise ValueError("Missing userId or items in request body")
    if not body["items"]:
        raise ValueError("Order items cannot be empty")
    if not isinstance(body["userId"], str):
        raise ValueError("Invalid userId")
    if not _valid_items(body["items"]):
        raise ValueError("Invalid items in request body")


def _valid_items(items):
    """Validate the items in the order."""
    if not isinstance(items, list):
        return False

    for item in items:
        if not isinstance(item, dict):
            return False
        if "productId" not in item or "quantity" not in item:
            return False
        if not isinstance(item["productId"], str) or not isinstance(
            item["quantity"], int
        ):
            return False
        if item["quantity"] <= 0:
            return False

    return True
