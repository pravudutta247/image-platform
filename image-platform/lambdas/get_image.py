from botocore.exceptions import ClientError
from common.db import table
from common.s3 import s3
from common.auth import get_tenant_id
from common.response import success, error

def handler(event, context):
    try:
        tenant_id = get_tenant_id(event)
        image_id = event.get("pathParameters", {}).get("image_id")

        if not image_id:
            return error("image_id is required")

        resp = table.get_item(
            Key={
                "tenant_id": tenant_id,
                "image_id": image_id
            }
        )

        item = resp.get("Item")
        if not item:
            return error("Image not found", 404)

        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": item["s3_bucket"],
                "Key": item["s3_key"]
            },
            ExpiresIn=3600
        )

        return success({"url": url})

    except ValueError as e:
        return error(str(e), 401)

    except ClientError:
        return error("AWS error", 500)

    except Exception:
        return error("Internal server error", 500)
