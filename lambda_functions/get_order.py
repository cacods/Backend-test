import json
import os

import boto3

try:
    # If running locally, import from the parent directory
    # TODO: is there a better way, without having to change the import?
    from lambda_functions.auth import InvalidTokenException, validate_token
    from lambda_functions.utils import DecimalEncoder
except ImportError:
    from auth import InvalidTokenException, validate_token
    from utils import DecimalEncoder

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("ORDERS_TABLE", "Orders"))


def lambda_handler(event, context):
    """Get an order by ID.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (LambdaContext): The context object provided by AWS Lambda.

    Returns:
        dict: The response object containing the status code and body.

    Raises:
        InvalidTokenException: If the provided token is invalid.
        Exception: For any other errors that occur during processing.
    """
    auth_token = event.get("headers", {}).get("Authorization")
    try:
        validate_token(auth_token)
    except InvalidTokenException as e:  # TODO: couldn't it be a decorator?
        return {
            "statusCode": 401,
            "body": json.dumps({"error": str(e)}),
        }

    try:
        order_id = event["pathParameters"]["id"]
        response = table.get_item(Key={"id": order_id})

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Order not found"}),
            }

        return {
            "statusCode": 200,
            "body": json.dumps(response["Item"], cls=DecimalEncoder),
        }
    except Exception as e:  # TODO: specify Exception (see other places)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
