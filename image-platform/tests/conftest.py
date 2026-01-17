import boto3
import pytest
import time
from botocore.exceptions import ClientError

LOCALSTACK = "http://localhost:4566"
TABLE_NAME = "images"
BUCKET = "images"

@pytest.fixture(scope="session", autouse=True)
def aws_setup():
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url=LOCALSTACK,
        region_name="us-east-1"
    )
    s3 = boto3.client(
        "s3",
        endpoint_url=LOCALSTACK,
        region_name="us-east-1"
    )

    # Wait for LocalStack
    for _ in range(10):
        try:
            dynamodb.list_tables()
            break
        except Exception:
            time.sleep(2)

    # Create S3 bucket
    try:
        s3.create_bucket(Bucket=BUCKET)
    except ClientError:
        pass

    # Create DynamoDB table if not exists
    if TABLE_NAME not in dynamodb.list_tables()["TableNames"]:
        dynamodb.create_table(
            TableName=TABLE_NAME,
            AttributeDefinitions=[
                {"AttributeName": "tenant_id", "AttributeType": "S"},
                {"AttributeName": "image_id", "AttributeType": "S"},
                {"AttributeName": "gsi_user_pk", "AttributeType": "S"},
                {"AttributeName": "gsi_tag_pk", "AttributeType": "S"},
                {"AttributeName": "created_at", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "tenant_id", "KeyType": "HASH"},
                {"AttributeName": "image_id", "KeyType": "RANGE"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "user-index",
                    "KeySchema": [
                        {"AttributeName": "gsi_user_pk", "KeyType": "HASH"},
                        {"AttributeName": "created_at", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "tag-index",
                    "KeySchema": [
                        {"AttributeName": "gsi_tag_pk", "KeyType": "HASH"},
                        {"AttributeName": "created_at", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )

        dynamodb.get_waiter("table_exists").wait(TableName=TABLE_NAME)
