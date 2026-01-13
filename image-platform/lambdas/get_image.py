from common.db import table
from common.s3 import s3

def handler(event, context):
    image_id = event["pathParameters"]["image_id"]

    item = table.get_item(Key={"image_id": image_id})["Item"]

    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": item["s3_bucket"],
            "Key": item["s3_key"]
        },
        ExpiresIn=3600
    )

    return {"statusCode": 200, "body": {"url": url}}
