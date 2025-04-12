import json

from lambda_functions.list_orders import lambda_handler


def test_list_orders_success(orders_table, valid_token):
    order_item_1 = {
        "id": "order_id_1",
        "userId": "test-user-1",
        "items": [
            {"product": "Book", "quantity": 2},
        ],
    }
    order_item_2 = {
        "id": "order_id_2",
        "userId": "test-user-2",
        "items": [{"product": "Pen", "quantity": 5}],
    }
    orders_table.put_item(Item=order_item_1)
    orders_table.put_item(Item=order_item_2)

    event = {
        "headers": {"Authorization": valid_token},
    }

    response = lambda_handler(event, None)
    assert response["statusCode"] == 200

    orders = json.loads(response["body"])
    assert len(orders) == 2


def test_list_orders_invalid_token(orders_table, invalid_token):
    order_item = {
        "id": "order_id_1",
        "userId": "test-user-1",
        "items": [
            {"product": "Book", "quantity": 2},
        ],
    }
    orders_table.put_item(Item=order_item)

    event = {
        "headers": {"Authorization": invalid_token},
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 401
    assert json.loads(response["body"])["error"] == "Unauthorized"


def test_list_orders_empty(orders_table, valid_token):
    event = {
        "headers": {"Authorization": valid_token},
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == []
