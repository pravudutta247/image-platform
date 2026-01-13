import boto3
import pytest
import time
from botocore.exceptions import ClientError

LOCALSTACK = "http://localhost:4566"

@pytest.fixture(scope="session", autouse=True)
def aws_setup():
    dynamodb = boto3.client("dynamodb", endpoint_url=LOCALSTACK, region_name="us-east-1")
    s3 = boto3.client("s3", endpoint_url=LOCALSTACK, region_name="us-east-1")

    # Wait for LocalStack to be ready
    for _ in range(10):
        try:
            dynamodb.list_tables()
            break
        except:
            time.sleep(2)

    # Create S3 bucket
    try:
        s3.create_bucket(Bucket="images")
    except ClientError:
        pass

    # Create DynamoDB table
    tables = dynamodb.list_tables()["TableNames"]

    if "images" not in tables:
        dynamodb.create_table(
            TableName="images",
            KeySchema=[
                {"AttributeName": "image_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "image_id", "AttributeType": "S"},
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "created_at", "AttributeType": "S"},
                {"AttributeName": "tag", "AttributeType": "S"}
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "user-index",
                    "KeySchema": [
                        {"AttributeName": "user_id", "KeyType": "HASH"},
                        {"AttributeName": "created_at", "KeyType": "RANGE"}
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                },
                {
                    "IndexName": "tag-index",
                    "KeySchema": [
                        {"AttributeName": "tag", "KeyType": "HASH"}
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )

        # Wait for table to be ACTIVE
        dynamodb.get_waiter("table_exists").wait(TableName="images")
