#!/bin/bash
set -e

ENDPOINT=http://localhost:4566
REGION=us-east-1
TABLE_NAME=images

echo "Creating DynamoDB table: $TABLE_NAME (multi-tenant)..."

aws --endpoint-url=$ENDPOINT dynamodb create-table \
  --table-name $TABLE_NAME \
  --region $REGION \
  --attribute-definitions \
    AttributeName=tenant_id,AttributeType=S \
    AttributeName=image_id,AttributeType=S \
    AttributeName=gsi_user_pk,AttributeType=S \
    AttributeName=gsi_tag_pk,AttributeType=S \
    AttributeName=created_at,AttributeType=S \
  --key-schema \
    AttributeName=tenant_id,KeyType=HASH \
    AttributeName=image_id,KeyType=RANGE \
  --global-secondary-indexes \
    '[
      {
        "IndexName": "user-index",
        "KeySchema": [
          {"AttributeName": "gsi_user_pk", "KeyType": "HASH"},
          {"AttributeName": "created_at", "KeyType": "RANGE"}
        ],
        "Projection": { "ProjectionType": "ALL" },
        "ProvisionedThroughput": {
          "ReadCapacityUnits": 5,
          "WriteCapacityUnits": 5
        }
      },
      {
        "IndexName": "tag-index",
        "KeySchema": [
          {"AttributeName": "gsi_tag_pk", "KeyType": "HASH"},
          {"AttributeName": "created_at", "KeyType": "RANGE"}
        ],
        "Projection": { "ProjectionType": "ALL" },
        "ProvisionedThroughput": {
          "ReadCapacityUnits": 5,
          "WriteCapacityUnits": 5
        }
      }
    ]' \
  --provisioned-throughput \
    ReadCapacityUnits=5,WriteCapacityUnits=5

echo "Waiting for table to become ACTIVE..."
aws --endpoint-url=$ENDPOINT dynamodb wait table-exists --table-name $TABLE_NAME

echo "DynamoDB table '$TABLE_NAME' created successfully."
