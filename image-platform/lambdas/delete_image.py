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
            return success({}, 204)  # idempotent delete

        s3.delete_object(
            Bucket=item["s3_bucket"],
            Key=item["s3_key"]
        )

        table.delete_item(
            Key={
                "tenant_id": tenant_id,
                "image_id": image_id
            }
        )

        return success({}, 204)

    except ValueError as e:
        return error(str(e), 401)

    except ClientError:
        return error("AWS error", 500)

    except Exception:
        return error("Internal server error", 500)
