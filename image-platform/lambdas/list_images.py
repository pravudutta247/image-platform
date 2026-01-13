from common.db import table

def handler(event, context):
    params = event.get("queryStringParameters", {})
    user_id = params.get("user_id")
    tag = params.get("tag")

    if user_id:
        resp = table.query(
            IndexName="user-index",
            KeyConditionExpression="user_id = :u",
            ExpressionAttributeValues={":u": user_id}
        )
    elif tag:
        resp = table.query(
            IndexName="tag-index",
            KeyConditionExpression="tag = :t",
            ExpressionAttributeValues={":t": tag}
        )
    else:
        resp = table.scan()

    return {
        "statusCode": 200,
        "body": resp["Items"]
    }
