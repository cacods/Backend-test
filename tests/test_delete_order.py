import json

from lambda_functions.delete_order import lambda_handler


def test_delete_order_success(orders_table, order_item, valid_token):
    orders_table.put_item(Item=order_item)

    event = {
        "headers": {"Authorization": valid_token},
        "pathParameters": {"id": order_item["id"]},
    }
    response = lambda_handler(event, None)
    item = orders_table.get_item(Key={"id": order_item["id"]})

    assert item["Item"]["status"] == "canceled"
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {
        "message": "Order canceled successfully",
        "order": order_item["id"],
    }


def test_delete_order_invalid_token(orders_table, order_item, invalid_token):
    orders_table.put_item(Item=order_item)

    event = {
        "headers": {"Authorization": invalid_token},
        "pathParameters": {"id": order_item["id"]},
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 401
    assert json.loads(response["body"])["error"] == "Unauthorized"


def test_delete_order_not_found(orders_table, valid_token):
    order_item = {
        "id": "test_order_id",
        "userId": "test-user-1",
        "items": [
            {"product": "Book", "quantity": 2},
        ],
    }
    orders_table.put_item(Item=order_item)

    event = {
        "headers": {"Authorization": valid_token},
        "pathParameters": {"id": "missing_id"},
    }
    response = lambda_handler(event, None)

    assert response["statusCode"] == 404
