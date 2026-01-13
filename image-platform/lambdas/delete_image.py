from common.db import table
from common.s3 import s3

def handler(event, context):
    image_id = event["pathParameters"]["image_id"]

    item = table.get_item(Key={"image_id": image_id})["Item"]

    s3.delete_object(Bucket=item["s3_bucket"], Key=item["s3_key"])
    table.delete_item(Key={"image_id": image_id})

    return {"statusCode": 204}
