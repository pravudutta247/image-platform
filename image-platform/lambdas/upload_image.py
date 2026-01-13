import uuid
import time
from common.db import table
from common.s3 import s3, BUCKET

def handler(event, context):
    body = event["body"]
    user_id = body["user_id"]
    file_bytes = body["file"]
    tag = body.get("tag", "general")

    image_id = str(uuid.uuid4())
    key = f"{user_id}/{image_id}.jpg"

    s3.put_object(Bucket=BUCKET, Key=key, Body=file_bytes)

    table.put_item(Item={
        "image_id": image_id,
        "user_id": user_id,
        "created_at": str(int(time.time())),
        "tag": tag,
        "s3_bucket": BUCKET,
        "s3_key": key
    })

    return {
        "statusCode": 200,
        "body": {
            "image_id": image_id,
            "s3_key": key
        }
    }
