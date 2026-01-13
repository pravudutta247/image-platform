aws --endpoint-url=http://localhost:4566 dynamodb create-table \
  --table-name images \
  --attribute-definitions \
    AttributeName=image_id,AttributeType=S \
    AttributeName=user_id,AttributeType=S \
    AttributeName=created_at,AttributeType=S \
    AttributeName=tag,AttributeType=S \
  --key-schema \
    AttributeName=image_id,KeyType=HASH \
  --global-secondary-indexes \
    '[
      {
        "IndexName": "user-index",
        "KeySchema": [
          {"AttributeName":"user_id","KeyType":"HASH"},
          {"AttributeName":"created_at","KeyType":"RANGE"}
        ],
        "Projection":{"ProjectionType":"ALL"},
        "ProvisionedThroughput":{"ReadCapacityUnits":5,"WriteCapacityUnits":5}
      },
      {
        "IndexName": "tag-index",
        "KeySchema": [
          {"AttributeName":"tag","KeyType":"HASH"}
        ],
        "Projection":{"ProjectionType":"ALL"},
        "ProvisionedThroughput":{"ReadCapacityUnits":5,"WriteCapacityUnits":5}
      }
    ]' \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
