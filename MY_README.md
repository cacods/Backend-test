# Requirements
- docker
- docker-compose
- The deployment process considers you have an AWS account and a default
profile configured with permission to create the resources used in the project.
- The commands listed bellow were exectued in a GNU/Linux environment with the Bash
shell. So probably they will work well in WSL environment.

# Summary
This project is a minimal order processing API that allows users to place orders
for products. It is built using AWS Lambda, DynamoDB, and API Gateway.
Since it's a simple REST API, we opted out to have each endpoint
as a separate Lambda function.
The API supports basic order management functionalities such as
creating, retrieving, listing, and deleting orders.

The project is designed to be deployed on AWS using the Serverless Application Model (SAM).
It includes a simple authentication mechanism using mocked JWT tokens. The API is built
using Python and follows RESTful practices.

The project also includes unit tests to ensure the functionality of the API endpoints.

# How to test
1. Clone the repository and run `./build.sh` in the project root folder.
The script is just a wrapper for the docker-compose command to build the
image and run the container.
```bash
$ ./build.sh
```
The docker-compose builds and deploys the SAM stack in AWS.
At the end of the output you will see the API endpoint URI and some examples
of how to test the API using `curl`.


2. Run unit tests
```bash
$ docker-compose exec sam-deployer pytest
```

3. Destroy de SAM stack

To delete the SAM stack just run `./destroy.sh` in the project root folder.
This will delete the SAM stack and stop the docker container.
At the end, it asks for deleting the Python image created by the docker-compose.
```bash
$ ./destroy.sh
```

_Note_: the stack is deployed on AWS eu-west-1 region by default.