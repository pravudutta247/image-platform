import boto3
import os

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1"
)

table = dynamodb.Table("images")
