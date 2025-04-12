# Requirements
- python>=3.10
- [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [sam cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

# How to test
1. Create an activate a python virtual environment
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

2. Install requirements
```bash
$ pip install -r requirements.txt
```

3. Run unit tests
```bash
$ pytest
```

4. Deploy in AWS and upload test data
4.1 Deploy in AWS
```bash
$ sam build && sam deploy --guided
```
Follow the instructions to build the SAM stack
- Type the stack name of your choice
- For the questions about the API Gateway authentication, e.g., `CreateOrderFunction has no authentication. Is this okay?`, you may respond "y". The authentication is made in the Lambda functions level, with a JWT mocked content.
- For the other questions you may respond "y".
- In the _Outputs_ section at the end of the deployment outputs you can see the API endpoint. You will use it to make manual tests.

4.2 Upload test data

It's needed to have the Users table preloaded to check for user ID when POSTing new Order
```bash
$ aws dynamodb put-item --table-name Users --item '{"id": {"S": "test-user-1"}, "name": {"S": "Alice"}}' --region eu-west-1
$ aws dynamodb put-item --table-name Users --item '{"id": {"S": "test-user-2"}, "name": {"S": "Bob"}}' --region eu-west-1
```
- This two commands adds two users for testing purposes.

5. Make manual tests

You can use any http command line client (or using some graphical tool like postman) to test the API

Sample tests using curl (notice that the authorization token is a mock token defined in the code):

5.1. Create order (`POST /orders`)
```bash
$ curl -H "Authorization: Bearer mock-user-1-token" -X POST <API_URI>/orders -H "Content-Type: application/json" -d '{
    "userId": "test-user-2",
    "items": [
      {"productId": "head phone", "quantity": 2},
      {"productId": "car", "quantity": 1}
    ]
  }'
```

5.2. List orders (`GET /orders`)
```bash
$ curl -H "Authorization: Bearer mock-user-1-token" <API_URI>/orders
```

5.3. Retrieve an order (`GET /orders/{id}`)
```bash
$ curl -H "Authorization: Bearer mock-user-1-token" <API_URI>/orders/<order_id>
```
Note: The "order_id" can be took from the DynamoDB table in AWS Console, listing the orders using `aws dynamodb` client, or getting the id after posting a new order

5.4. Delete an order (will be marked as "canceled") (`DELETE /orders/{id}`)
```bash
$ curl -H "Authorization: Bearer mock-user-1-token" -X DELETE <API_URI>/orders/<order_id>
```
Note: The "order_id" can be took from the DynamoDB table in AWS Console, listing the orders using `aws dynamodb` client, or getting the id after posting a new order

You can test for errors. Try creating an order with wrong items format, doing requests without authorization token, POSTing an order without the user id, or an invalid user, etc.

**AWS costs doing the manual tests**: the costs incurred for this tests is very low because the request for DynamoDB are configured as Pay Per Request. The costs associated with the requests for the API Gateway endpoints, and Lambda functions are very low too.

6. Destroy de SAM stack
```bash
$ sam delete
```
This will destroy all the SAM stack AWS infrastructure.
