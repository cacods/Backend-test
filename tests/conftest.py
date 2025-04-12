import os

import boto3
import pytest

from moto import mock_aws


@pytest.fixture
def users_table():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
        table = dynamodb.create_table(
            TableName="Users",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        # Preload test users
        table.put_item(Item={"id": "test-user-1", "name": "Alice"})
        table.put_item(Item={"id": "test-user-2", "name": "Bob"})
        os.environ["USERS_TABLE"] = "Users"
        yield table


@pytest.fixture
def orders_table(users_table):
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
        table = dynamodb.create_table(
            TableName="Orders",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        os.environ["ORDERS_TABLE"] = "Orders"
        yield table


@pytest.fixture
def dynamodb_tables(users_table, orders_table):
    yield {"users_table": users_table, "orders_table": orders_table}


@pytest.fixture
def order_item():
    yield {
        "id": "test_order_id",
        "userId": "test-user-1",
        "items": [
            {"productId": "Book", "quantity": 2},
            {"productId": "Pen", "quantity": 5},
        ],
    }


@pytest.fixture
def valid_token():
    yield "Bearer mock-user-1-token"


@pytest.fixture
def invalid_token():
    yield "Bearer fake-token"
