import json

from lambda_functions.create_order import lambda_handler


def test_create_order_success(orders_table, order_item, valid_token):
    event = {
        "headers": {"Authorization": valid_token},
        "body": json.dumps(order_item),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 201
    assert "id" in json.loads(response["body"])


def test_create_order_invalid_token(orders_table, order_item, invalid_token):
    event = {
        "headers": {"Authorization": invalid_token},
        "body": json.dumps(order_item),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 401
    assert json.loads(response["body"])["error"] == "Unauthorized"


def test_create_order_invalid_input(orders_table, valid_token):
    event = {
        "headers": {"Authorization": valid_token},
        "body": json.dumps({"invalid": "data"}),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    assert (
        json.loads(response["body"])["error"]
        == "Missing userId or items in request body"
    )


def test_create_order_user_not_found(orders_table, valid_token):
    event = {
        "headers": {"Authorization": valid_token},
        "body": json.dumps(
            {
                "userId": "non-existent-user",
                "items": [{"productId": "Book", "quantity": 2}],
            }
        ),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"])["error"] == "User not found"


def test_create_order_empty_items(orders_table, valid_token):
    event = {
        "headers": {"Authorization": valid_token},
        "body": json.dumps({"userId": "test-user-1", "items": []}),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"])["error"] == "Order items cannot be empty"


def test_create_order_wrong_items_format_1(orders_table, valid_token):
    event = {
        "headers": {"Authorization": valid_token},
        "body": json.dumps(
            {
                "userId": "test-user-1",
                "items": [
                    {"prod": "Book", "qtty": 2},
                    {"product": "Pen", "quantidade": 5},
                ],
            }
        ),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"])["error"] == "Invalid items in request body"


def test_create_order_wrong_items_format_2(orders_table, valid_token):
    event = {
        "headers": {"Authorization": valid_token},
        "body": json.dumps(
            {
                "userId": "test-user-1",
                "items": [{"productId": "Book", "quantity": "two"}],
            }
        ),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"])["error"] == "Invalid items in request body"


def test_create_order_wrong_items_format_3(orders_table, valid_token):
    event = {
        "headers": {"Authorization": valid_token},
        "body": json.dumps(
            {"userId": "test-user-1", "items": [{"productId": 1, "quantity": 2}]}
        ),
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"])["error"] == "Invalid items in request body"
