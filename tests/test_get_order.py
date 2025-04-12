import json

from lambda_functions.get_order import lambda_handler


def test_get_order_success(orders_table, order_item, valid_token):
    orders_table.put_item(Item=order_item)

    event = {
        "headers": {"Authorization": valid_token},
        "pathParameters": {"id": order_item["id"]},
    }
    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == order_item


def test_get_order_invalid_token(orders_table, order_item, invalid_token):
    orders_table.put_item(Item=order_item)

    event = {
        "headers": {"Authorization": invalid_token},
        "pathParameters": {"id": order_item["id"]},
    }
    response = lambda_handler(event, None)

    assert response["statusCode"] == 401
    assert json.loads(response["body"])["error"] == "Unauthorized"


def test_get_order_not_found(orders_table, order_item, valid_token):
    orders_table.put_item(Item=order_item)

    event = {
        "headers": {"Authorization": valid_token},
        "pathParameters": {"id": "missing_id"},
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 404
